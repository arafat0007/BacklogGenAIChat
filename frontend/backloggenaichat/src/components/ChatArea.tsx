import React, { useState, useEffect } from 'react';
import '../styles/ChatArea.css';
import MessageInput from './MessageInput';
import Message from './Message';
import {BASE_URL, STREAM_RESPONSE_ERROR, HOME_URL, LOGIN_URL} from '../constants/constant';
import IStreamJSON from '../interfaces/IStreamJSON';
import IMessage from '../interfaces/IMessage';
import FeedbackModal from './Feedback';

const ChatArea: React.FC = () => {
  // チャットセッションが作成されているかどうかを表すフラグ
  const [isSessionCreated, setIsSessionCreated] = useState(false);
  // フィードバックモーダルが開いているかどうかを表すフラグ
  const [isFeedbackModalOpen, setIsFeedbackModalOpen] = useState(false);
  // チャットの送信者のメールアドレス
  const [email, setEmail] = useState('');
  // チャットで送受信されたメッセージの配列
  const [messages, setMessages] = useState<IMessage[]>([]);
  // 入力が無効になっているかどうかを表すフラグ
  const [isInputDisabled, setIsInputDisabled] = useState(false);

  /**
   * 新しいチャットセッションを作成し、chat_idをlocalStorageに保存します。
   */
  const handleCreateSession = async () => {
    try {
      const response = await fetch(BASE_URL+'/create_chat', { // 新しいチャットセッションを作成
        method: 'POST', // HTTP POSTリクエスト
        headers: { 'Content-Type': 'application/json' }, // JSONボディ
        body: JSON.stringify({ email }), // emailをJSONボディに含む
      });
      const data = await response.json(); // JSONレスポンスボディをパース
      console.log(data); // サーバのレスポンスをログ
      localStorage.setItem('chatId', data.chat_id); // chat_idをlocalStorageに保存
      setIsSessionCreated(true); // チャットエリアを有効化
    } catch (error) {
      console.error('Error creating session::', error); // エラーをログ
    }
  };

  /**
   * 現在のチャットセッションを終了し、フィードバックモーダルを開きます。
   */
  const handleEndSession = () => {
    // ユーザーにチャットのフィードバックを求めるフィードバックモーダルを開く
    setIsFeedbackModalOpen(true);
  };

    /**
     * ASSISTANTにメッセージを送信し、レスポンスを待機します。
     * @param query ASSISTANTに送信するメッセージ
     */
    const sendMessage = async (query: string) => {
      try {
        // ユーザーメッセージとASSISTANTの初期レスポンスメッセージを作成
        const userMessage: IMessage = { sender: 'user', text: query, isAnswerLoading: false, isStreaming: false };
        const assistantMessage: IMessage = { sender: 'assistant', text: 'Analysing the query', isAnswerLoading: true, isStreaming: false };
        setMessages((prevMessages) => [...prevMessages, userMessage, assistantMessage]);

        // ASSISTANTのレスポンスを待つ間、入力を無効化
        setIsInputDisabled(true);
        await sleep(1);
        autoScrollBar();

        const storedChatId = localStorage.getItem('chatId');

        // ASSISTANTにメッセージを送信
        const response = await fetch(BASE_URL + `/query`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ chat_id: storedChatId, query, email }),
        });

        if (!response.ok || !response.body) {
          // ASSISTANTが失敗した場合、エラーメッセージを表示
          console.log('QA failed...');
          assistantMessage.text = STREAM_RESPONSE_ERROR;
          assistantMessage.isAnswerLoading = false;
          assistantMessage.isStreaming = false;
          setMessages((prevMessages) => [...prevMessages]);
          // 入力を有効化
          setIsInputDisabled(false);
          await sleep(1);
          autoScrollBar();
          return;
        }

        // ASSISTANTのレスポンスをストリームとして受け取る
        const reader = response.body.getReader();
        const textDecoder = new TextDecoder();
        let buffer = '';
        let unterminatedJson = '';
        let rawData = '';

        // ストリームから受け取ったJSONオブジェクトを処理する
        while (true) {
          const { done, value } = await reader.read();
          if (done) {
            // バックエンド処理が終了しても、のこりのJSONデータがあればコンソールに表示されます。
            if (unterminatedJson) {
              console.log(`unterminated json: ${unterminatedJson}`);
            }

            // ASSISTANTのメッセージをストリームではないものとしてマーク
            setMessages((prevMessages) => {
              const updatedMessages = [...prevMessages];
              updatedMessages[updatedMessages.length - 1].isStreaming = false;
              return updatedMessages;
            });

            break;
          }

          // decodeしたデータ
          rawData = textDecoder.decode(value, { stream: true });
          unterminatedJson += rawData;

          // APIのレスポンスをデシリアライズする
          const responseJsons: IStreamJSON[] = [];
          unterminatedJson = await parseJSON(responseJsons, unterminatedJson);

          // GPTストリームで複数のJSONを返却煤可能性があるのでJSONをループで処理する
          for (const item of responseJsons) {
            const { status, message } = item;
            // ステータスがprocessingの場合は、処理メッセージを表示する
            if (status === 'processing') {
              // ASSISTANTのメッセージを更新
              assistantMessage.text = message;
              setMessages((prevMessages) => [...prevMessages]);
            } else {
              // またはレスポンスデータを表示する
              // ASSISTANTのレスポンスをバッファに追加
              buffer += message;
              // ASSISTANTのメッセージを更新
              setMessages((prevMessages) => {
                const updatedMessages = [...prevMessages];
                updatedMessages[updatedMessages.length - 1].text = buffer;
                updatedMessages[updatedMessages.length - 1].isAnswerLoading = false;
                updatedMessages[updatedMessages.length - 1].isStreaming = true;
                return updatedMessages;
              });

              await sleep(60);
              autoScrollBar();
            }
          }
        }

        setIsInputDisabled(false);
        await sleep(1);
        autoScrollBar();

      } catch (error) {
        console.error('Error sending message:', error);
      }
    };


    /**
     * JSON文字列をパースし、残りの文字列を返す
     * @param {IStreamJSON[]} responseJsons JSONをパースした配列
     * @param {string} jsons パース対象のJSON文字列
     * @returns {Promise<string>} パースに成功した場合は空の文字列、失敗した場合はそのままの文字列
     */
    const parseJSON = async (responseJsons: IStreamJSON[], jsons: string): Promise<string> => {
      // 文字列が空の場合は空の文字列を返す
      if (!jsons) {
        return "";
      }

      try {
        // JSON文字列をパースする
        const parsedResponse: IStreamJSON = JSON.parse(jsons);
        // パースに成功した場合は空の文字列を返す
        responseJsons.push(parsedResponse);
        return "";
      } catch (error: any) {
        // パースに失敗した場合のエラーメッセージを取得する
        const errorMessage = error.message;
        // エラーがJSONが不完全である場合のエラーでない場合は、そのままの文字列を返す
        if (!errorMessage.includes("Unexpected non-whitespace character after JSON")) {
          return jsons;
        }
        // JSONパースに失敗した位置を取得する
        const position = parseInt(errorMessage.split("at position ")[1].split(" ")[0]);
        // 文字列を分割する
        const firstJson = jsons.substring(0, position);
        const secondJson = jsons.substring(position);

        // 1つ目のJSONをパースして配列に追加する
        const parsedResponse: IStreamJSON = JSON.parse(firstJson);
        responseJsons.push(parsedResponse);
        // 残りの文字列を再帰的にパースする
        return parseJSON(responseJsons, secondJson);
      }
    };

    /**
     * 指定したミリ秒数待つ関数
     *
     * @param {number} ms 待つ時間(ミリ秒)
     * @returns {Promise<void>} 待ち終わるまで処理をブロックするPromise
     */
    const sleep = async (ms: number): Promise<void> => {
      // setTimeoutを使用して指定したミリ秒数待つ
      return new Promise(resolve => setTimeout(resolve, ms));
    };

    /**
     * 新しいメッセージが追加されたときに、自動的にチャットエリアの一番下までスクロールする。
     */
    const autoScrollBar = () => {
      // メッセージエリアを格納するHTML要素を取得する
      const messageArea = document.getElementById('scroll-area');
      // メッセージエリアの要素が存在する場合
      if (messageArea) {
        // メッセージエリアの一番下までスクロールする
        messageArea.scrollTo({
          // メッセージエリアの一番下までスクロールする
          top: messageArea.scrollHeight,
          // スクロールアニメーションをスムーズにする
          behavior: 'smooth',
        });
      }
    };

    /**
     * フィードバックの送信を処理します。
     *
     * @param {string} feedback ユーザーからのフィードバックメッセージ
     * @param {number} rating ユーザーの評価 (1-10)
     */
    const handleFeedbackSubmit = async (feedback: string, rating: number) => {
      // LocalStorageからチャットIDを取得する
      const storedChatId = localStorage.getItem('chatId');
      setIsFeedbackModalOpen(false); // フィードバックモーダルを閉じる
      setIsSessionCreated(false); // チャットエリアを無効化
      setMessages([]); // メッセージリストをクリアする

      try {
        // フィードバックをバックエンドAPIに送信する
        await fetch(BASE_URL+'/create_feedback', { // フィードバックを送信する
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ 'chat_id' : storedChatId, 'content': feedback, 'rating': rating }),
        });
      } catch (error) {
        console.error('Feedback submission error:', error);
      }
    };

    useEffect(() => {
      // URLパラメータからメールアドレスを取得する
      const urlParams = new URLSearchParams(window.location.search);
      const email = urlParams.get('email');

      // メールアドレスを LocalStorage に保存する
      if (email) {
        localStorage.setItem('email', email);
        setEmail(email);
        window.location.href = HOME_URL;
      }
      else{
        const email = localStorage.getItem('email');
  
        if (!email) {
          window.location.href = LOGIN_URL;
        }else{
          setEmail(email);
        }
      }
    }, []);

    /**
    /**
     * フィードバックモーダルを閉じる
     */
    const handleFeedbackClose = () => {
      setIsFeedbackModalOpen(false); // フィードバックモーダルを閉じる
    };

  return (
    <div className="chat-area">
      <div className="chat-header d-flex justify-content-between align-items-center">
        <div className="d-flex align-items-center justify-content-center flex-grow-1">
          <h2 className="chat-title">Backlog Help Center</h2>
        </div>
        {isSessionCreated && <button className="btn btn-warning" onClick={handleEndSession}>End Session</button>}
      </div>

      {!isSessionCreated ? (
        <div className="creating-session">
          <div className="session-text">Need help about Backlog? Start a conversation with our super chat by creating session.</div>
          <button className="btn btn-success" onClick={handleCreateSession}>Create Session</button>
        </div>
      ) : (
        <div className="message-container">
          <div className='message-area' id='scroll-area'>
            {messages.map((message, index) => (
              <React.Fragment key={index}><Message sender={message.sender} text={message.text} isAnswerLoading={message.isAnswerLoading} isStreaming={message.isStreaming} /></React.Fragment>
            ))}
          </div>
          <MessageInput onSendMessage={sendMessage} isInputDisabled={isInputDisabled}/>
        </div>
      )}
      <FeedbackModal onFeedbackSubmit={handleFeedbackSubmit} isOpen={isFeedbackModalOpen} onClose={handleFeedbackClose}/>
    </div>
  );
};

export default ChatArea;
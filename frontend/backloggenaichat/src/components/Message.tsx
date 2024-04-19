import React from 'react';
import { SyncLoader, SquareLoader } from 'react-spinners';

interface MessageProps {
  sender: string;
  text: string;
  isAnswerLoading: boolean;
  isStreaming: boolean;
}

/**
 * メッセージコンポーネント
 * チャットにメッセージを表示し、送信者に応じて適切なCSSクラスを適用します
 * @param {string} sender メッセージの送信者 (userまたはASSISTANT)
 * @param {string} text メッセージのテキスト
 * @param {boolean} isAnswerLoading ASSISTANTからのレスポンスが現在ロード中であるかどうか
 * @param {boolean} isStreaming ASSISTANTからのストリーミングレスポンスが現在進行中であるかどうか
 */
const Message: React.FC<MessageProps> = ({ sender, text, isAnswerLoading, isStreaming }) => {
  // 現在ロード中でない場合にのみ、改行で区切られたテキストをパラグラフ配列に分割
  const paragraphs:string[] = !isAnswerLoading && text && text.length > 0 ? text.split('\n\n') : [];
  // メッセージのCSSクラスを送信者に基づいて決定
  const messageClass = sender === 'user' ? 'user-message' : 'assistant-message';

  return (
    <div className={`message ${messageClass}`}>
      {/* ロード中の場合、ローディングスピナーを表示 */}
      {isAnswerLoading ? 
        (
          <div className='loading-container'>
            <span>{text}</span>
            <SyncLoader color='#000' size={3} />
          </div>
        ) : 
        (
          <>
            {/* ロード中でない場合、パラグラフをマップして表示 */}
            {paragraphs && paragraphs.map((paragraph, index) => (
              <p key={index}>
                {paragraph}
                {/* 最後のパラグラフで、ストリーミング中ならばストリーミングスピナーを表示 */}
                {index === paragraphs.length - 1 && isStreaming && <SquareLoader color='#000' size={10} cssOverride={{display: 'inline-block'}} speedMultiplier={1} />}
              </p>
            ))}
          </>
        )}
    </div>
  );
};

export default Message;
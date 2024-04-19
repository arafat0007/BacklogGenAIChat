import React, { useState } from 'react';
import '../styles/MessageInput.css';

interface MessageInputProps {
  onSendMessage: (message: string) => void;
  isInputDisabled: boolean;
}

/**
 * メッセージ入力エリア
 * @param onSendMessage ASSISTANTにメッセージを送信するためのコールバック関数
 * @param isInputDisabled 入力フィールドを無効化する場合true
 */
const MessageInput: React.FC<MessageInputProps> = ({ onSendMessage, isInputDisabled }) => {
  // 入力テキストを格納する状態
  const [inputText, setInputText] = useState('');

  /**
   * 入力値変更時のイベントハンドラ
   * @param e 変更イベント
   */
  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInputText(e.target.value);
  };

  /**
   * メッセージ送信ボタンクリック時のイベントハンドラ
   */
  const handleSendMessage = () => {
    // 入力テキストをコールバック関数に渡す
    onSendMessage(inputText);
    setInputText(''); // 送信後、入力フィールドをクリアする
  };

  /**
   * テキストエリアのキーダウンイベントハンドラ
   * @param e キーダウンイベント
   */
  const handlekeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    // Ctrl + Enterでメッセージ送信
    if (e.key === 'Enter' && e.ctrlKey) {
      handleSendMessage();
    }
    // Enterキーで、CtrlやShiftを押していない場合、メッセージ送信
    else if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault(); // デフォルトのEnter動作を抑制
      handleSendMessage();
    }
  };

  return (
    <div className="message-input">
      <textarea
        className="form-control"
        placeholder="Type your query here. user Shift + Enter for line break."
        value={inputText}
        disabled={isInputDisabled}
        onChange={handleInputChange}
        onKeyDown={handlekeyDown}
      />
      <button
        className="btn btn-primary ml-2"
        disabled={isInputDisabled}
        onClick={handleSendMessage}
      >
        Send
      </button>
    </div>
  );
};

export default MessageInput;

import React, { useState, ChangeEvent } from 'react';
import { Button, Modal, Form } from 'react-bootstrap';
import '../styles/Feedback.css';

interface FeedbackModalProps {
    isOpen: boolean;
    onFeedbackSubmit: (feedback: string, rating: number) => void;
    onClose: () => void;
}

/**
* フィードバックモーダルコンポーネント
*
* @param isOpen フィードバックモーダルが開いているかどうか
* @param onFeedbackSubmit フィードバックと評価を受け取り、フィードバックを送信するコールバック関数
* @param onClose フィードバックモーダルを閉じるコールバック関数
*/
const FeedbackModal: React.FC<FeedbackModalProps> = ({ isOpen, onFeedbackSubmit, onClose }) => {
  // ユーザのフィードバック
  const [feedback, setFeedback] = useState<string>('');
  // ユーザの評価 (1-10)
  const [rating, setRating] = useState<number>(10);

  /**
   * フィードバックテキストエリアの変更を検知
   *
   * @param e フィードバックテキストエリアの変更イベント
   */
  const handleFeedbackChange = (e: ChangeEvent<HTMLTextAreaElement>): void => {
    setFeedback(e.target.value);
  };

  /**
   * フィードバック送信処理
   */
  const handleSubmit = (): void => {
    onFeedbackSubmit(feedback, rating);
    setFeedback('');
    setRating(10);
  };

  /**
   * フィードバックモーダルを閉じる処理
   *
   * フィードバックテキストエリアと評価を初期化し、コールバック関数を呼び出す
   */
  const handleClose = (): void => {
    // フィードバックテキストエリアと評価を初期化
    setFeedback('');
    setRating(10);
    // コールバック関数を呼び出す
    onClose();
  };

  return (
    <>
      {/* フィードバックモーダル */}
      <Modal show={isOpen} onHide={handleClose} centered>
        <Modal.Header closeButton>
          <Modal.Title className='mx-auto'>Backlog Help Center Feedback</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <p className="greeting-text">Thank you for taking the time to provide feedback!</p>
          <Form.Group>
            <Form.Control
              as="textarea"
              rows={4}
              cols={60}
              placeholder="Tell us your thoughts..."
              value={feedback}
              onChange={handleFeedbackChange}
            />
          </Form.Group>
          <Form.Group>
            <Form.Label className='mt-3'>Rating:</Form.Label>
            <div className="rating-container">
              {/* 各評価をループ */}
              {[...Array(10)].map((_, index) => (
                <span
                  key={index} // React.js の要件
                  className={`rating-star ${rating === index + 1 ? 'selected' : ''}`} // 選択時に CSS クラスを追加
                  onClick={() => setRating(index + 1)} // クリックイベントの処理
                >
                  &#9733; {/* スターアイコン */}
                </span>
              ))}
            </div>
          </Form.Group>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="primary" onClick={handleSubmit}>
            Submit
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
};

export default FeedbackModal;
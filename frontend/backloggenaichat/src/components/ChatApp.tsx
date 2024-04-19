import React from 'react';
import ChatArea from './ChatArea';

/**
 * チャットアプリのルートコンポーネントです。
 * 中央寄せのカードの中にChatAreaコンポーネントを含むコンテナのdivを持っています。
 */
const ChatApp: React.FC = () => {
  return (
    <div className="container-fluid"> {/* container-fluidはアプリをフル幅にする */}
      <div className="row">  {/* rowはフレックスコンテナ */}
        <div className="col-md-8 mx-auto"> {/* col-md-8はカードを中央寄せにして、12列のうち8列を使う */}
          <div className="card border-0"> {/* border-0はデフォルトの border を削除する */}
            <div className="card-body">  {/* card-bodyはChatAreaを中央寄せする */}
              <ChatArea /> {/* アプリのメインコンポーネント */}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatApp;



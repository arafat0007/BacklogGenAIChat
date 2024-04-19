# BacklogGenAIChat

## Why Generate AI Chat Backlog

BacklogGenAIChat is a project aimed at enhancing user experience by providing an AI-powered chat service for efficiently addressing user queries related to backlog issues. The primary objective is to streamline the process of finding solutions, thereby reducing the need for direct customer service interactions and improving overall efficiency.

### Issues Found:

- Users may struggle to find relevant solutions within the provided links, leading to frustration and time wastage.
- Direct calls to customer service may increase due to the difficulty in finding solutions independently, resulting in an overflow of requests.

### Solution:

The project focuses on providing a seamless solution where users can effortlessly obtain solutions without extensive reading or searching. By leveraging the RAG (Retrieve, Analyze, Generate) function and GPT (Generative Pre-trained Transformer) technology, users' queries can be comprehensively addressed.

### Effects of the Service:

- Increased product impressions in the backlog, enhancing the overall product value.
- Reduction in the pressure on customer service by mitigating the influx of direct requests.

## Technology Stack

- **Backend:** Python, FastAPI
- **Frontend:** Typescript, React.js
- **Database:** MySQL
- **ORM:** SQLAlchemy
- **Tools:** Chat GPT 4, Langchain, Tiktoken, etc.

## Setups

### Database Setup:

1. Navigate to the directory containing the `docker-compose.yml` file (in ```/backend```).
2. Run the following command to start the containers defined in the `docker-compose.yml` file:
   ```
   docker-compose up
   ```
    This command will initiate the MySQL container named `BacklogGenAIChat` with the specified configurations.

3. Optionally, to run the containers in detached mode (in the background), use the `-d` flag:
   ```
   docker-compose up -d
   ```

4. To stop the containers, use the following command:
   ```
   docker-compose down
   ```

   If not using Docker, follow the necessary database setup instructions in the `docker-compose.yml` file and install MySQL into the system.

### Backend Setup:

1. Create a file named `.env` in the ```/backend``` directory.
2. Set the following variables in the `.env` file:
   ```
   DATABASE_URL=mysql+pymysql://root:backlog@localhost/BacklogGenAIChat
   OPENAI_KEY=YOUR_OPENAI_KEY
   CLIENT_ID=NULAB_CLIENT_ID
   CLIENT_SECRET=NULAB_CLIENT_SECRET
   REDIRECT_URI=http://localhost:8000/oauth_code
   ```
3. Create a virtual environment by running the following command in the terminal in the ```/backend``` directory:
   ```
   python -m venv venv
   ```
4. Activate the virtual environment:
   - For Command Prompt:
     ```
     venv\Scripts\activate
     ```
   - For PowerShell:
     ```
     .\venv\Scripts\Activate.ps1
     ```
5. Ensure that `(venv)` is displayed at the start of the directory path.
6. Install all the dependencies of the backend service by running:
   ```
   pip install -r requirements.txt
   ```
7. Create an `app_log` folder in the ```/backend``` directory to store log files.
8. Start the backend by running:
   ```
   uvicorn main:app
   ```
   **Ensure that the database is running in Docker; otherwise, it will throw errors.**

9. Access all the endpoints at [http://localhost:8000/docs](http://localhost:8000/docs).

### Frontend Setup:

1. Navigate to the Project Directory (`/frontend/backloggenaichat`).
2. Install Dependencies by running either of the following commands:
   ```
   npm install
   ```
3. Run the Development Server:
   ```
   npm start
   ```
4. Access the frontend at [http://localhost:3000/](http://localhost:3000/)

## System Access Flow:

1. **OAuth Login:**
   - When accessing Welcome page(http://localhost:3000) for the first time, it will take back the user to the Nulab Oauth page. On user's permission as "Allow", it will return back to the welcome page(http://localhost:3000).

2. **Welcome to Backlog Help Center:**
   - Upon accessing the platform, users are greeted with a simple interface, welcoming them to the "Backlog Help Center."

3. **Create Session:**
   - To initiate a conversation regarding backlog issues, users are prompted to click the "Create Session" button, positioned at the center of the page.

4. **Query Submission:**
   - Users are presented with a text input area, encouraging them to type their queries in a textbox. Upon typing, the textbox subtly glows with a soothing color, indicating user engagement.

5. **Send Query:**
   - An "Send" button accompanies the query input area, inviting users to submit their questions.

6. **AI Analysis and Response:**
   - The BacklogGenAIChat service processes the query using cutting-edge AI technology behind the scenes. Meanwhile, users enjoy a captivating animation, symbolizing the system's analytical prowess.

7. **Response Display:**
   - The generated response elegantly appears on the screen, accompanied by visually appealing graphics and smooth transitions, ensuring a delightful user experience.

8. **Seamless Interaction:**
   - Users can continue the conversation seamlessly, with each interaction feeling intuitive and engaging.

9. **End Session:**
   - When users are satisfied with the assistance provided, they can conclude the session by clicking the "End Session" button, positioned at the top-right corner of the page.

10. **Feedback Submission:**
   - After ending the session, users are encouraged to share their valuable feedback through a visually striking feedback form.

11. **Return to Backlog Help Center:**
    - Upon submitting feedback, users are redirected to the "Backlog Help Center".

# BacklogGenAIChat

## AI チャットのバックログを生成する理由

BacklogGenAIChat は、バックログに関連するユーザーのクエリを効率的に処理するための AI パワード チャット サービスを提供することで、ユーザー エクスペリエンスを向上させることを目指したプロジェクトです。主な目的は、ソリューションを見つけるプロセスを合理化し、直接顧客サービスのやり取りの必要性を減らし、全体的な効率を向上させることです。

### 問題点:

- 提供されたリンク内で関連するソリューションを見つけるのが難しいため、ユーザーが苦労することがあり、時間の無駄が発生します。
- ソリューションを独自に見つける難しさにより、顧客サービスへの直接的なコールが増加し、リクエストのオーバーフローが発生する可能性があります。

### ソリューション:

プロジェクトは、ユーザーが広範囲な読書や検索なしで簡単にソリューションを入手できるシームレスなソリューションを提供することに焦点を当てています。RAG (Retrieve, Analyze, Generate) 関数と GPT (Generative Pre-trained Transformer) テクノロジーを活用することで、ユーザーのクエリを包括的にアドレスします。

### サービスの効果:

- バックログ内での製品の印象が増加し、全体的な製品価値が向上します。
- 直接的なリクエストのインフルックスを緩和することで、顧客サービスへの圧力が軽減されます。

## テクノロジースタック

- **バックエンド:** Python, FastAPI
- **フロントエンド:** Typescript, React.js
- **データベース:** MySQL
- **ORM:** SQLAlchemy
- **ツール:** Chat GPT 4, Langchain, Tiktoken など

## セットアップ

### データベースのセットアップ:

1. ```/backend``` ディレクトリ内にある `docker-compose.yml` ファイルが含まれるディレクトリに移動します。
2. 次のコマンドを実行して、`docker-compose.yml` ファイルで定義されたコンテナを起動します:
   ```
   docker-compose up
   ```
   このコマンドは、指定された構成で `BacklogGenAIChat` という名前の MySQL コンテナを初期化します。

3. コンテナをバックグラウンドで実行する場合は、`-d` フラグを使用して次のコマンドを実行します:
   ```
   docker-compose up -d
   ```

4. コンテナを停止するには、次のコマンドを使用します:
   ```
   docker-compose down
   ```

   Docker を使用しない場合は、`docker-compose.yml` ファイル内の必要なデータベースのセットアップ手順に従い、システムに MySQL をインストールします。

### バックエンドのセットアップ:

1. ```/backend``` ディレクトリに `.env` という名前のファイルを作成します。
2. `.env` ファイルに次の変数を設定します:
   ```
   DATABASE_URL=mysql+pymysql://root:backlog@localhost/BacklogGenAIChat
   OPENAI_KEY=YOUR_OPENAI_KEY
   CLIENT_ID=NULAB_CLIENT_ID
   CLIENT_SECRET=NULAB_CLIENT_SECRET
   REDIRECT_URI=http://localhost:8000/oauth_code
   ```
3. ターミナルで ```/backend``` ディレクトリ内で次のコマンドを実行して、仮想環境を作成します:
   ```
   python -m venv venv
   ```
4. 仮想環境をアクティブにします:
   - コマンド プロンプトの場合:
     ```
     venv\Scripts\activate
     ```
   - PowerShell の場合:
     ```
     .\venv\Scripts\Activate.ps1
     ```
5. ディレクトリ パスの先頭に `(venv)` が表示されることを確認します。
6. 次のコマンドを実行して、バックエンド サービスのすべての依存関係をインストールします:
   ```
   pip install -r requirements.txt
   ```
7. ```/backend``` ディレクトリに `app_log` フォルダーを作成して、ログファイルを保存します。
8. 次のコマンドを実行してバックエンドを起動します:
   ```
   uvicorn main:app
   ```
   **Docker でデータベースが実行されていることを確認してください。さもなければ、エラーが発生します。**

9. [http://localhost:8000/docs](http://localhost:8000/docs) ですべてのエンドポイントにアクセスします。

### フロントエンドのセットアップ:

1. プロジェクトディレクトリ (`/frontend/backloggenaichat`) に移動します。
2. 次のコマンドのいずれかを実行して依存関係をインストールします:
   ```
   npm install
   ```
3. 開発サーバーを実行します:
   ```
   npm start
   ```
4. [http://localhost:3000/](http://localhost:3000/) でフロントエンドにアクセスします。

## システム アクセス フロー:

1. **OAuthログイン:**
   - 初めてウェルカムページ（http://localhost:3000）にアクセスすると、ユーザーはNulab OAuthページに戻されます。 ユーザーが「許可」を選択すると、ウェルカムページ（http://localhost:3000）に戻ります。

2. **バックログ ヘルプ センターへようこそ:**
   - プラットフォームにアクセスすると、シンプルなインターフェイスが表示され、「バックログ ヘルプ センター」へようこそと表示されます。

3. **セッションの作成:**
   - バックログの問題に関する会話を開始するには、ページの中央に配置された「セッションを作成」ボタンをクリックします。

4. **クエリの送信:**
   - テキスト入力エリアが表示され、テキストボックスにクエリを入力するよう促されます。入力すると、テキストボックスは静かな色で光り、ユーザーの関与を示します。

5. **クエリの送信:**
   - クエリ入力エリアに「送信」ボタンが表示され、ユーザーは簡単に質問を送信できます。

6. **AI の分析と応答:**
   - BacklogGenAIChat サービスがクエリを処理し、裏で先進の AI テクノロジーを使用します。その間、ユーザーは分析力を象徴する魅力的なアニメーションを楽しむことができます。

7. **応答の表示:**
   - 生成された応答が画面に優雅に表示され、見栄えの良いグラフィックとスムーズなトランジションが付属し、楽しいユーザーエクスペリエンスが保証されます。

8. **シームレスなインタラクション:**
   - ユーザーはシームレスに会話を続けることができ、各インタラクションが直感的で魅力的に感じます。

9. **セッションの終了:**
   - ユーザーが提供されたサポートに満足した場合は、ページの右上隅に配置された「セッションの終了」ボタンをクリックしてセッションを終了できます。

10. **フィードバックの送信:**
   - セッションの終了後、ユーザーは目を引くフィードバックフォームを通じて貴重なフィードバックを共有するよう促されます。

11. **バックログ ヘルプ センターに戻る:**
    - フィードバックを送信した後、ユーザーは「バックログ ヘルプ センター」にリダイレクトされます。
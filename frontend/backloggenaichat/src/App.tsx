import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import ChatApp from './components/ChatApp';
import AuthError from './components/AuthError';
import { Helmet } from 'react-helmet';

const App: React.FC = () => {
  return (
    <Router>
      <div className="app">
        <Helmet>
          <title>Backlog Help Center</title>
          <meta name="description" content="It is a help center for Backlog where users can ask FAQs about Backlog." />
          <link rel="icon" type='image/x-icon' href="/backlog.ico" />
        </Helmet>
        <Routes>
          <Route path="/oauth_error" Component={AuthError} />
          <Route path="/" Component={ChatApp} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;

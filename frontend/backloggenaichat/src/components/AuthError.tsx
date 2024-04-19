import React from 'react';

const AuthError: React.FC = () => {
  return (
    <div>
      <h1>Auth Error</h1>
      <p>Oops! Something went wrong. Try accessing <a href="http://localhost:3000">Home page</a> again.</p>
    </div>
  );
};

export default AuthError;

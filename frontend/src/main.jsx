import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import { AuthProvider } from './context/AuthContext.jsx'
import { GoogleOAuthProvider } from '@react-oauth/google'
import './index.css'

createRoot(document.getElementById('root')).render(
  <GoogleOAuthProvider clientId="605039480451-79spfo1apkqvfo2foq6aq6t59002osob.apps.googleusercontent.com">
    <AuthProvider>
      <App />
    </AuthProvider>
  </GoogleOAuthProvider>
)

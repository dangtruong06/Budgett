import { BrowserRouter, Routes, Route } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import Dashboard from './pages/Dashboard';
import ExpenseForm from './pages/ExpenseForm';
import LandingPage from './pages/LandingPage'
import ProtectedRoute from './components/ProtectedRoute'


function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<LandingPage/>} />
        <Route path='/login' element={<LoginPage/>} />
        <Route path='/register' element={<RegisterPage/>} />
        <Route path='/dashboard' element={<ProtectedRoute><Dashboard/></ProtectedRoute>} />
        <Route path='/expenses/new' element={<ProtectedRoute><ExpenseForm/></ProtectedRoute>} />
        <Route path='/expenses/:id/edit' element={<ProtectedRoute><ExpenseForm/></ProtectedRoute>} />

      </Routes>
    </BrowserRouter>

  )
}

export default App

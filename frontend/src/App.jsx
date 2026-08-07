import { BrowserRouter, Routes, Route } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import Dashboard from './pages/Dashboard';
import ExpenseForm from './pages/ExpenseForm';


function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route path='/login' element={<LoginPage/>} />
        <Route path='/register' element={<RegisterPage/>} />
        <Route path='/dashboard' element={<Dashboard/>} />
        <Route path='/expenses/new' element={<ExpenseForm/>} />
        <Route path='/expenses/:id/edit' element={<ExpenseForm/>} />

      </Routes>
    </BrowserRouter>

  )
}

export default App

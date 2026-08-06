import { useState } from 'react'
import { useNavigate } from 'react-router-dom';
import api from '../api/axios'

function RegisterPage(){
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleRegister = async (e) => {
        e.preventDefault()

        try{
            const response = await api.post('/register', { email, password });
            navigate('/login')
        }
        catch(error){
            console.error(error.response?.data)
        }
    };

    return (
        <div>
            <h1>Register Page</h1>
            <form onSubmit={ handleRegister }>
                <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="email"/>
                <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="password"/>
                <input type="submit" />
            </form>
        </div>
    )
}

export default RegisterPage;
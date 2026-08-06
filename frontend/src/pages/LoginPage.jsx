import { useState } from 'react';
import api from '../api/axios'
import { useAuth } from '../context/AuthContext'

function LoginPage(){
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const { login } = useAuth();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try{
            const response = await api.post('/login', { email, password }); 
            login(response.data.access_token);
            
        } catch (error){
            console.error(error.response?.data);
        }

    };

    return (
        <div>
            <h1>Login Page</h1>
            <form onSubmit={handleSubmit}>
                <input 
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="email@email.com"
                />
                <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="password"
                />
                <button type="submit">Log In</button>

            </form>

        </div>



    );
}

export default LoginPage;
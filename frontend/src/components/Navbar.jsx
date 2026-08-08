import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

function Navbar() {
    const location = useLocation();
    const navigate = useNavigate();
    const { token, logout } = useAuth()

    const handleLogout = () => {
        logout();
        navigate('/');
    };

    return (
        <nav className="flex items-center justify-between px-6 py-4 border-b border-gray-100 bg-white">
            <Link to="/" className="text-lg font-medium text-emerald-700 lowercase">
                budgett
            </Link>
            <div className="flex items-center gap-2">
                {token ? (
                    <button
                        onClick={handleLogout}
                        className="px-4 py-2 text-sm text-gray-600 hover:text-gray-900"
                    >
                        Log out
                    </button>
                ) : (
                    <>
                        {location.pathname !== '/login' && (
                            <Link to="/login" className="px-4 py-2 text-sm text-gray-600 hover:text-gray-900">
                                Log in
                            </Link>
                        )}
                        {location.pathname !== '/register' && (
                            <Link to="/register" className="px-4 py-2 text-sm font-medium text-white bg-emerald-600 rounded-lg hover:bg-emerald-700">
                                Sign up
                            </Link>
                        )}
                    </>
                )}
            </div>
        </nav>
    );
}

export default Navbar;
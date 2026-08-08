import { Link, useLocation } from 'react-router-dom';

function Navbar() {
    const location = useLocation();

    return (
        <nav className="flex items-center justify-between px-6 py-4 border-b border-gray-100 bg-white">
            <Link to="/" className="text-lg font-medium text-emerald-700 lowercase">
                budgett
            </Link>
            <div className="flex items-center gap-2">
                {location.pathname !== '/login' && (
                    <Link
                        to="/login"
                        className="px-4 py-2 text-md text-gray-600 hover:text-gray-900"
                    >
                        Log in
                    </Link>
                )}
                {location.pathname !== '/register' && (
                    <Link
                        to="/register"
                        className="px-4 py-2 text-md font-medium text-white bg-emerald-600 rounded-lg hover:bg-emerald-700"
                    >
                        Sign up
                    </Link>
                )}
            </div>
        </nav>
    );
}

export default Navbar;
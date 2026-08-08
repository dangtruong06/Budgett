import { Link } from "react-router-dom";
import { Plus, Folder, BarChart3 } from "lucide-react";
import NavBar from '../components/Navbar'

function LandingPage() {
    const year = new Date().getFullYear()
  return (
    <div className="min-h-screen bg-white flex flex-col">
      {/* Nav */}
      <NavBar/>

      {/* Hero */}
      <section className="flex-1 flex flex-col md:flex-row items-center gap-16 px-6 md:px-16 py-16 max-w-6xl mx-auto w-full">
        <div className="flex-1">
          <h1 className="text-3xl md:text-4xl font-medium text-gray-900 leading-tight mb-4">
            Track spending without the spreadsheet
          </h1>
          <p className="text-gray-600 mb-6 max-w-md">
            Log expenses, organize them by category, and watch your habits
            take shape.
          </p>
          <Link
            to="/register"
            className="inline-block px-6 py-3 text-sm font-medium text-white bg-emerald-600 rounded-lg hover:bg-emerald-700"
          >
            Get started free
          </Link>
        </div>

        {/* Preview card */}
        <div className="flex-1 w-full bg-emerald-50 rounded-2xl p-6 flex flex-col gap-3">
          <div className="flex justify-between text-sm text-emerald-900">
            <span>Groceries</span>
            <span className="font-medium">$84.20</span>
          </div>
          <div className="flex justify-between text-sm text-emerald-900">
            <span>Transit</span>
            <span className="font-medium">$32.00</span>
          </div>
          <div className="flex justify-between text-sm text-emerald-900">
            <span>Coffee</span>
            <span className="font-medium">$14.50</span>
          </div>
        </div>
      </section>

      {/* Feature strip */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6 px-6 md:px-16 pb-16 max-w-6xl mx-auto w-full">
        <div className="text-center">
          <Plus className="mx-auto mb-2 text-emerald-600" size={22} />
          <p className="text-sm text-gray-600">Add expenses</p>
        </div>
        <div className="text-center">
          <Folder className="mx-auto mb-2 text-emerald-600" size={22} />
          <p className="text-sm text-gray-600">Sort by category</p>
        </div>
        <div className="text-center">
          <BarChart3 className="mx-auto mb-2 text-emerald-600" size={22} />
          <p className="text-sm text-gray-600">Track spending habits</p>
        </div>
      </section>

      {/* Footer */}
      <footer className="text-center text-xs text-gray-400 py-6 border-t border-gray-100">
        Tony Dang · budgett · { year }
      </footer>
    </div>
  );
}

export default LandingPage;
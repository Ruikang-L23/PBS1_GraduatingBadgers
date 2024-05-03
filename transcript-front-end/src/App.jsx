// Import React components and Router elements
import './App.css';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navigation from "./components/Navigation";
import UploadPage from "./components/UploadPage";
import HomePage from "./components/HomePage";
import Viewer from "./components/Viewer";
import ErrorPage from "./components/ErrorPage";

// Main App component defining the route structure
export default function App() {

  return (
      <BrowserRouter>
        {/* Setup the Navigation component as a layout with nested routes */}
        <Routes>
          <Route path="/" element={<Navigation />}>
            <Route index element={<HomePage />}></Route> // Home page at root
            <Route path="upload" element={<UploadPage />}></Route> // Upload page
            <Route path="viewer" element={<Viewer />}></Route> // Viewer page
            <Route path="*" element={<ErrorPage />}></Route> // Fallback for unmatched routes
          </Route>
        </Routes>
      </BrowserRouter>
  );

}
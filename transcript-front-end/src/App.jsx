import './App.css';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navigation from "./components/Navigation";
import UploadPage from "./components/UploadPage";
import HomePage from "./components/HomePage";
import Viewer from "./components/Viewer";
import ErrorPage from "./components/ErrorPage";

export default function App() {

  return (
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Navigation />}>
            <Route index element={<HomePage />}></Route>
            <Route path="upload" element={<UploadPage />}></Route>
            <Route path="viewer" element={<Viewer />}></Route>
            <Route path="*" element={<ErrorPage />}></Route>
          </Route>
        </Routes>
      </BrowserRouter>
  );

}
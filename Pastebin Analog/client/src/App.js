import './App.css';
import {
  BrowserRouter as Router,
  Routes,
  Route
} from 'react-router-dom'

import CreateNote from './pages/CreateNote/CreateNote';
import NoteDetails from './pages/NoteDetails/NoteDetails';
import { AuthProvider } from './context/AuthContext';


function App() {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route path='/' element={<CreateNote/>}/>
          <Route path='/:hash' element={<NoteDetails/>}/>
        </Routes>
      </AuthProvider>
    </Router>
  );
}

export default App;

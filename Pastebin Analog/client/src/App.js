import './App.css';
import {
  BrowserRouter as Router,
  Routes,
  Route
} from 'react-router-dom'

import CreateNote from './pages/CreateNote/CreateNote';
import NoteDetails from './pages/NoteDetails/NoteDetails';


function App() {
  return (
    <Router>
      <Routes>
        <Route path='/' element={<CreateNote/>}/>
        <Route path='/:hash' element={<NoteDetails/>}/>
      </Routes>
    </Router>
  );
}

export default App;

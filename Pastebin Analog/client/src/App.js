import './App.css';
import {
  BrowserRouter as Router,
  Routes,
  Route
} from 'react-router-dom'

import CreateNote from './pages/CreateNote/CreateNote';


function App() {
  return (
    <Router>
      <Routes>
        <Route path='/' element={<CreateNote/>}/>
      </Routes>
    </Router>
  );
}

export default App;

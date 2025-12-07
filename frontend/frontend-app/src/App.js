import { Routes, Route, BrowserRouter } from 'react-router-dom';
import Home from "./Components/Pages/Home/Home";
import SignIn from './Components/Pages/SignIn/SignIn';
import SignUp from './Components/Pages/SignUp/SignUp';
import Test from './Components/Pages/Test/Test';


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/signin' element={ < SignIn /> }/>
        <Route path='/signup' element={ < SignUp /> }/>
        <Route path='/test' element={ < Test /> } />
      </Routes>
    </BrowserRouter>
  );
}

export default App;

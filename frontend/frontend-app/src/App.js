import { Routes, Route, BrowserRouter } from 'react-router-dom';
import Home from "./Components/Pages/Home/Home";
import SignIn from './Components/Pages/SignIn/SignIn';
import SignUp from './Components/Pages/SignUp/SignUp';
import Test from './Components/Pages/Test/Test';
import Posts from "./Components/Pages/Posts/Posts";


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/signin' element={ < SignIn /> }/>
        <Route path='/signup' element={ < SignUp /> }/>
        <Route path='/test' element={ < Test /> } />
        <Route path='/posts' element={ < Posts /> } />
      </Routes>
    </BrowserRouter>
  );
}

export default App;

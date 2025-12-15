import { Routes, Route, BrowserRouter, useParams } from 'react-router-dom';
import Home from "./Components/Pages/Home/Home";
import SignIn from './Components/Pages/SignIn/SignIn';
import SignUp from './Components/Pages/SignUp/SignUp';
import Test from './Components/Pages/Test/Test';
import Posts from "./Components/Pages/Posts/Posts";
import Post from './Components/Pages/Post/Post';
import Profile from './Components/Pages/Profile/Profile';

function PostWrap() {
    const {postId} = useParams();
    console.log(`PostId is ${postId}`);
    return <Post postId={postId} />
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/signin' element={ < SignIn /> }/>
        <Route path='/signup' element={ < SignUp /> }/>
        <Route path='/test' element={ < Test /> } />
        <Route path='/posts' element={ < Posts /> } />
        <Route path='/post/:postId' element = {< PostWrap />} />
        <Route path='/profile' element = {< Profile />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;

import Menu from "../Menu/Menu";

// const api = "http://localhost:80/users";


function getUsers(){
fetch("/users")
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.text();
  })
  .then(data => {
    console.log('Data received:', data);
  })
  .catch(error => {
    console.error('Error fetching data:', error);
  });
}

function Test() {
    return (
        <>
            <header class="header">
                <h1 class="header-h1">Page with tests</h1>
            </header>
            <Menu />
            <p>{getUsers()}</p>
        </>
    );
};

export default Test;
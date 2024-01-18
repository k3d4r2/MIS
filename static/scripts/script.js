
async function waitForSomeTime() {
  console.log('Start');
  
  // Wait for 2 seconds
  await new Promise(resolve => setTimeout(resolve, 4000));

  console.log('End');
}

async function fetchUserProfile(uid) {
    const url = '/get-user/' + uid;

    try {
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        return data
    } catch (error) {
        return {"Error" : "something went wrong weeee"}
    }
}

function makeAdmin(uid) {
    const url = '/make-admin/' + uid;

    console.log(url);

    fetch(url, {
        method: "GET"
    })
    .then(response => {
        console.log(response);
        return Promise.resolve();
    })
    .then(() => {
        toggleUserProfile(uid);
        return Promise.resolve();
    })
    .then(() => {
        updateUsersList();
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


function removeAdmin(uid) {
    const url = '/remove-admin/' + uid;

    console.log(url);

    fetch(url, {
        method: "GET"
    })
    .then(response => {
        console.log(response);
        return Promise.resolve();
    })
    .then(() => {
        toggleUserProfile(uid);
        return Promise.resolve();
    })
    .then(() => {
        updateUsersList();
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function toggleUserProfile(uid) {
    // get element
    const userProfileContainer = document.getElementById("user-" + uid);
    userProfileContainer.style.opacity = 1;
    userProfileContainer.style.display = (userProfileContainer.style.display === 'none' || userProfileContainer.style.display === '') ? 'flex' : 'none';
}

function showLoader() {
    const loader = document.getElementsByClassName("loader")[0];
    loader.style.display = 'block';
    console.log("Loader shown")
}

function hideLoader() {
    const loader = document.getElementsByClassName("loader")[0];
    loader.style.display = 'none';
    console.log("Loader hidden")
}

function updateUsersList() {
    // update the users list
    const listContainer = document.getElementById("users-list");
    console.log(listContainer);
    fetch("/users-list", {
        method: "GET"
    })
        .then(response => {
            return response.text();
        })
        .then((html) => {
            showLoader();
            return html;
        })
        .then(html => {
            listContainer.innerHTML = html;
            return Promise.resolve();
        }).then(() => {
            hideLoader();
        });
}

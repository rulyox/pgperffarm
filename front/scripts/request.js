const baseUrl = 'http://localhost:8000/';

const endpoints = {
    home: baseUrl + 'overview/'
};

const sendRequest = (url, callback) => {

    const httpRequest = new XMLHttpRequest();
    httpRequest.open('GET', url);
	httpRequest.send();

    httpRequest.onreadystatechange = () => {

        if (httpRequest.readyState === XMLHttpRequest.DONE) {

            if (httpRequest.status === 200) {
                const response = JSON.parse(httpRequest.response);
                callback(response);
            } 
            else {
                console.log(httpRequest.status);
            }
        }
    }

};

import React from "react";
import "./App.css";

class App extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      genre_detected: {},
      data_received: false,
    };

    this.handleUploadImage = this.handleUploadImage.bind(this);
  }

  handleUploadImage(ev) {
    ev.preventDefault();

    const data = new FormData();
    data.append("file", this.uploadInput.files[0]);
    console.log(this.uploadInput.files[0]);
    // data.append('filename', this.fileName.value);

    fetch("http://localhost:5000/data", {
      method: "POST",
      // mode: 'no-cors',
      body: data,
    }).then((response) => {
      response.json().then((body) => {
        console.warn(body);
        this.setState({ genre_detected: body, data_received: true });
      });
    });
  }

  render() {
    return (
      <div className="app">
        <div className="form">
          <h2>Select a Music File</h2>
          <br />
          <form onSubmit={this.handleUploadImage}>
            <div>
              <input
                ref={(ref) => {
                  this.uploadInput = ref;
                }}
                type="file"
              />
            </div>
            <br />
            <div>
              <button>Check</button>
            </div>
          </form>
          {this.state.data_received ? (
            <div className="output">
              <p className="winner">{this.state.genre_detected.data}</p>
            </div>
          ) : null}
        </div>
      </div>
    );
  }
}

export default App;

import React, { useState, useRef } from 'react';
import { ReactSketchCanvas } from 'react-sketch-canvas'; // New import
import axios from 'axios';
import './App.css';

function App() {
  const [prediction, setPrediction] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isEmpty, setIsEmpty] = useState(true);
  const canvasRef = useRef(null);

  const handleDrawChange = () => {
    setIsEmpty(false);
  };

  const handleClear = () => {
    if (canvasRef.current) {
      canvasRef.current.clearCanvas(); // Use the new clear method
    }
    setPrediction(null);
    setIsEmpty(true);
  };

  const handlePredict = async () => {
    if (canvasRef.current) {
      // Use the new export method to get a base64 image string
      const imageData = await canvasRef.current.exportImage('png');
      
      setIsLoading(true);
      setPrediction(null);

      try {
        const response = await axios.post('[https://pixel-mind-backend.onrender.com/predict](https://pixel-mind-backend.onrender.com/predict)', {
          imageData: imageData // Send the base64 image data
        });
        setPrediction(response.data.prediction);
      } catch (error) {
        console.error("Error predicting:", error);
        setPrediction("Error");
      } finally {
        setIsLoading(false);
      }
    }
  };

  return (
    <div className="App">
      <h1>Pixel-Mind</h1>
      <div className="canvas-container">
        <ReactSketchCanvas
          ref={canvasRef}
          strokeWidth={15}
          strokeColor="black"
          canvasColor="white"
          height="280px"
          width="280px"
          onChange={handleDrawChange}
          className="canvas"
        />
      </div>
      <div className="button-container">
        <button className="clear-button" onClick={handleClear}>Clear</button>
        <button 
          className="predict-button" 
          onClick={handlePredict}
          disabled={isEmpty || isLoading} 
        >
          Predict
        </button>
      </div>
      <div className="result-container">
        {isLoading ? (
          <p className="loading-text">Predicting...</p>
        ) : (
          prediction !== null && (
            <h2 className="prediction-text">
              Prediction:
              <span className="prediction-result">{prediction}</span>
            </h2>
          )
        )}
      </div>
    </div>
  );
}

export default App;
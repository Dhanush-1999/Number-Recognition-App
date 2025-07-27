import React, { useState, useRef } from 'react';
import CanvasDraw from 'react-canvas-draw';
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
      canvasRef.current.clear();
    }
    setPrediction(null);
    setIsEmpty(true);
  };

  const handlePredict = async () => {
    if (canvasRef.current) {
      const drawingData = canvasRef.current.getSaveData();

      setIsLoading(true);
      setPrediction(null);

      try {
        const response = await axios.post('http://localhost:5000/predict', {
         imageData : drawingData
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
      <h1>Draw a Digit</h1>
      <div className="canvas-container">
        <CanvasDraw
          ref={canvasRef}
          brushColor="black"
          brushRadius={10}
          lazyRadius={0}
          canvasWidth={280}
          canvasHeight={280}
          gridColor="rgba(255, 255, 255, 0)"
          onChange={handleDrawChange} 
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

import './App.css';
import React from 'react';
import { FaceLivenessDetector } from '@aws-amplify/ui-react-liveness';
import { Loader, ThemeProvider } from '@aws-amplify/ui-react';
import { Amplify } from 'aws-amplify';
import '@aws-amplify/ui-react/styles.css';
import awsexports from './aws-exports';

Amplify.configure(awsexports);

function App() {
  const [loading, setLoading] = React.useState(true);
  const [sessionId, setSessionId] = React.useState(null);

  // Reemplazamos la lógica para crear la sesión de liveness
  React.useEffect(() => {
    const fetchCreateLiveness = async () => {
      try {
        // Llamada a la API de FastAPI para crear la sesión
        const response = await fetch('http://127.0.0.1:8000/api/create-liveness-session');
        const data = await response.json();
        console.error('voy por aqui++++++++++++s:', data.sessionId);
        
        setSessionId(data.sessionId);
        setLoading(false);
      } catch (error) {
        console.error('Error al crear la sesión de liveness:', error);
      }
    };

    fetchCreateLiveness();
  }, []);

  const handleAnalysisComplete = async () => {
    try {
      // Llamada a la API de FastAPI para obtener los resultados
      const response = await fetch(`http://127.0.0.1:8000/api/get-liveness-results?sessionId=${sessionId}`);
      const data = await response.json();

      /*
       * Aquí debes interpretar los resultados que recibes de la API
       * Puedes realizar alguna acción adicional según el valor de "confidence" o "status"
       */
      console.log('Resultados de liveness:', data);

      // Por ejemplo:
      if (data.status === 'COMPLETED' && data.confidence > 0.9) {
        console.log('El usuario está vivo con alta confianza');
      } else {
        console.log('No se pudo verificar liveness');
      }
    } catch (error) {
      console.error('Error al obtener los resultados de liveness:', error);
    }
  };

  return (
    <ThemeProvider>
      {loading ? (
        <Loader />
      ) : (
        <FaceLivenessDetector
          sessionId={sessionId}
          region="us-east-1"
          onAnalysisComplete={handleAnalysisComplete}
          onError={(error) => {
            console.error('Error en la detección de liveness:', error);
          }}
        />
      )}
    </ThemeProvider>
  );
}

export default App;

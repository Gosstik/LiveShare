import React, { createContext, useContext } from 'react';
import ApiClient from './ApiClient';

// Create the API client instance
const apiClient = new ApiClient();

// Create context
export const ApiContext = createContext(null);

// Provider component
export const ApiProvider = ({ children }) => {
  return (
    <ApiContext.Provider value={apiClient}>
      {children}
    </ApiContext.Provider>
  );
};

// Hook for using the API client
export const useApi = () => {
  const context = useContext(ApiContext);
  if (!context) {
    throw new Error('useApi must be used within an ApiProvider');
  }
  return context;
};

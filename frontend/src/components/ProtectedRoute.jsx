import { Navigate } from 'react-router-dom';

function ProtectedRoute({ children }) {
  const user = localStorage.getItem('varisetuUser');
  
  if (!user) {
    return <Navigate to="/login" replace />;
  }
  
  return children;
}

export default ProtectedRoute;

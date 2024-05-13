import { postRequest } from '@/lib/fetch';
import jwt from 'jsonwebtoken';

export const useAuth = () => {
  const onRegister = async (data, callback) => {
    try {
      const response = await postRequest({
        endPoint: '/auth/register',
        formData: data,
        isFormData: false,
      });
      console.log('🚀 ~ onRegister ~ response:', response);
      callback(response);
      return response;
    } catch (error) {
      console.log(error);
    }
  };
  const onLogin = async (data, callback) => {
    try {
      const response = await postRequest({
        endPoint: '/auth/login',
        formData: data,
        isFormData: false,
      });
      console.log('🚀 ~ onLogin ~ response:', response);
      callback(response);
      return response;
    } catch (error) {
      console.log(error);
    }
  };

  // const getSession = async () => {
  //   try {

  //   }
  // }

  return {
    onRegister,
    onLogin,
  };
};

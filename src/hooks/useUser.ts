import { getRequest, postRequest } from '@/lib/fetch';
import jwt from 'jsonwebtoken';

export const useUser = () => {
  const onGetAvatar = async (callback) => {
    try {
      const response = await getRequest({
        endPoint: '/user/avatar/',
      });
      console.log('🚀 ~ onGetAvatar ~ response:', response);
      callback(response);
      return response;
    } catch (error) {
      console.log(error);
    }
  };
  const onPostCv = async (data, callback) => {
    try {
      const response = await postRequest({
        endPoint: '/user/cv/',
        formData: data,
        isFormData: true,
      });
      console.log('🚀 ~ onPostCv ~ response:', response);
      callback(response);
      return response;
    } catch (error) {
      console.log(error);
    }
  };
  const onGetCv = async (callback) => {
    try {
      const response = await getRequest({
        endPoint: '/user/cv/',
      });
      console.log('🚀 ~ onGetCv ~ response:', response);
      callback(response);
      return response;
    } catch (error) {
      console.log(error);
    }
  };
  return {
    onGetAvatar,
    onPostCv,
    onGetCv,
  };
};

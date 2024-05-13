import { getRequest } from '@/lib/fetch';
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
  return {
    onGetAvatar,
  };
};

import { getRequest } from '@/lib/fetch';

export const useJob = () => {
  const onGetJobs = async (page: number) => {
    try {
      const response = await getRequest({
        endPoint: '/jobs/?page=' + page,
      });
      console.log('🚀 ~ onGetJobs ~ response:', response);
      return response.data;
    } catch (error) {
      console.log(error);
    }
  };

  return {
    onGetJobs,
  };
};

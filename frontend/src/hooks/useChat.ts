import { getRequest, postRequest } from '@/lib/fetch';

export const useChat = () => {
  const onPostChat = async (data) => {
    try {
      const response = await postRequest({
        endPoint: '/chatbot/',
        formData: data,
        isFormData: false,
      });
      console.log('🚀 ~ onPostChhhat ~ response:', response);
      return response.data;
    } catch (error) {
      console.log(error);
    }
  };

  return {
    onPostChat,
  };
};

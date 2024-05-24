import axiosClient from './axios';

export const getRequest = async ({ endPoint }) => {
  const res = await axiosClient.get(endPoint);
  return res;
};

export const postRequest = async ({ endPoint, formData, isFormData }) => {
  try {
    const res = await axiosClient.post(
      endPoint,
      isFormData ? formData : JSON.stringify(formData),
      isFormData && {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    console.log('🚀 ~ postRequest ~ res:', res);
    return res;
  } catch (error) {
    return error;
  }
};
export const putRequest = async ({ endPoint, formData, isFormData }) => {
  const res = await axiosClient.put(
    endPoint,
    isFormData ? formData : JSON.stringify(formData),
    isFormData && {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    }
  );
  return res;
};
export const deleteRequest = async ({ endPoint }) => {
  const res = await axiosClient.delete(endPoint);
  return res;
};

import axiosClient from '@/lib/axios';
import { getRequest, postRequest } from '@/lib/fetch';
import axios from 'axios';
import jwt from 'jsonwebtoken';

export async function POST(req: Request) {
  const body = await req.json();
  if (!body) return new Response('no body', { status: 400 });
  try {
    const response = await postRequest({
      endPoint: process.env.NEXT_PUBLIC_BACKEND_URL + '/signup/',
      formData: body,
      isFormData: false,
    });
    console.log('response: ' + response.status);
    if (response.status == 201) {
      console.log('User created successfully!');
      return new Response(
        JSON.stringify({
          message: 'User created succesfully!',
          payload: response.data,
          status: 200,
        })
      );
    } else if (response.status == 500) {
      console.log('Error status 500');
      if (response.data.message.includes('EMAIL_EXISTS')) {
        console.log('Email already exists');
        return new Response('Email already exists', { status: 400 });
      } else {
        console.log('Error when creating user, not email exists');
        return new Response('Error when creating user', { status: 500 });
      }
    } else {
      return new Response('Error when creating user', { status: 500 });
    }
  } catch (error: any) {
    let e = error;
    if (error.response) {
      e = error.response.data; // data, status, headers
      if (error.response.data && error.response.data.error) {
        e = error.response.data.error; // my app specific keys override
      }
    } else if (error.message) {
      e = error.message;
    } else {
      e = 'Unknown error occured';
    }
    console.log('🚀 ~ POST ~ e:', e);
    return new Response('error', { status: 500 });
  }

  return new Response('hello world');
}

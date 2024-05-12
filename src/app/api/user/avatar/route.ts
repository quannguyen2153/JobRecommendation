import axiosClient from '@/lib/axios';
import { getRequest } from '@/lib/fetch';
import axios from 'axios';
import jwt from 'jsonwebtoken';

export async function GET() {
  try {
    const response = await getRequest({
      endPoint: process.env.NEXT_BACKEND_URL + '/user/avatar/',
    });
    if (response.status == 200) {
      return new Response(
        JSON.stringify({
          message: 'User created succesfully!',
          payload: response.data,
          status: 200,
        })
      );
    } else {
      return new Response('Error when fetching user avatar data', {
        status: 500,
      });
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
    console.log('🚀 ~ GET ~ e:', e);
    return new Response('error', { status: 500 });
  }
}

import { postRequest } from '@/lib/fetch';
import jwt from 'jsonwebtoken';
import { AuthOptions } from 'next-auth';
import CredentialsProvider from 'next-auth/providers/credentials';
const options: AuthOptions = {
  //SIGN IN CHAY TRUOC JWT, TRONG SIGNIN SE RETURN 1 THANG USER, JWT CHAY TRUOC SESSION
  // Configure one or more authentication providers
  session: {
    strategy: 'jwt',
  },
  providers: [
    CredentialsProvider({
      name: 'Credentials',
      credentials: {
        username: { label: 'Username', type: 'text' },
        password: { label: 'Password', type: 'password' },
      },
      async authorize(credentials) {
        const { email, password } = credentials as unknown as {
          email: string;
          password: string;
        };

        const body = { email, password };
        const response = await postRequest({
          endPoint: process.env.NEXT_BACKEND_URL + '/signin',
          formData: body,
          isFormData: false,
        });

        if (response.status !== 200)
          throw new Error('Email or password is incorrect');
        const user = response.data;
        if (user.password !== password || user.email !== email)
          throw new Error('Email or password is incorrect');

        return user;
      },
    }),

    // ...add more providers here
  ],

  callbacks: {
    //first it'll run the jwt function, the jwt function will return the token , then in the session function we can access the token
    async jwt({ token, user, trigger, session }) {
      console.log('🚀 ~ file: options.ts:154 ~ jwt ~ user:', user);
      console.log('🚀 ~ file: options.ts:154 ~ jwt ~ token:', token);
      if (trigger === 'update') {
        return { ...token, ...session.user };
      }
      if (user) {
        token.id = user.id;
        token.name = user.name;
        token.email = user.email;
      }
      //user is from the oauth config or in the credentials setting options

      //return final token
      return token;
    },
    async session({ token, session }) {
      // if (!userFind) {
      //   return {
      //     redirectTo: `/auth/login?email=${session?.user.email}&name=${session?.user.name}`,
      //   };
      // }
      console.log('token in session: ', token);
      if (session.user) {
        (session.user as { id: string }).id = token.id as string;
        (session.user as { name: string }).name = token.name as string;
        (session.user as { email: string }).email = token.email as string;
      }
      return session;
    },
  },
  pages: {
    signIn: '/login',
  },
};
export default options;

'use client';
import { useForm } from 'react-hook-form';

import {
  cn,
  regexPasswordNumber,
  regexPasswordSpecial,
  regexPasswordUpperCase,
} from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { AiFillEye, AiFillEyeInvisible } from 'react-icons/ai';
import { useEffect, useState } from 'react';
import { useAuth } from '@/hooks/useAuth';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormMessage,
} from '@/components/ui/form';
import * as z from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { Loader, Router } from 'lucide-react';
import 'react-toastify/dist/ReactToastify.css';
import { ToastContainer, toast } from 'react-toastify';
import { setCookie } from 'cookies-next';

//quan ly form: react-hook-form
//validate form: zod

const formSchema = z
  .object({
    username: z.string().min(1, {
      message: 'Username is required',
    }),
    password: z
      .string()
      .min(1, {
        message: 'Password is required',
      })
      .min(8, { message: 'Password must contains at least 8 characters' })
      .regex(regexPasswordSpecial, {
        message: 'Password must contains at least 1 special character',
      })
      .regex(regexPasswordNumber, {
        message: 'Password must contains at least 1 number',
      })
      .regex(regexPasswordUpperCase, {
        message: 'Password must contains at least 1 uppercase character',
      }),
    email: z
      .string()
      .min(1, {
        message: 'Email is required',
      })
      .email({ message: 'Invalid email' }),
    confirmPassword: z.string().min(1, {
      message: 'Confirm password is required',
    }),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: 'Passwords do not match',
    path: ['confirmPassword'],
  });
const Register = ({ className }: { className?: string }) => {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
    },
  });
  const { onRegister, onLogin } = useAuth();
  const [show, setShow] = useState({
    password: false,
    confirmPassword: false,
  });
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const router = useRouter();

  async function onSubmit(data) {
    console.log(data);
    //Remove confirmPassword field
    const { confirmPassword, ...rest } = data;
    setIsLoading(true);
    onRegister(rest, (response) => {
      console.log('response:' + response);
      setIsLoading(false);
      if (response.status === 200) {
        toast.success('User created successfully!');
        //Start login using new account
        const { username, ...loginData } = rest;
        onLogin(loginData, (response) => {
          console.log('response:' + response);
          setIsLoading(false);
          if (response.status == 200) {
            const payload = response.data.payload;
            console.log('payload:' + JSON.stringify(payload));
            const token = payload.token;
            // localStorage.setItem('token', token);
            // localStorage.setItem('user', JSON.stringify(payload.data));
            setCookie('token', token);
            setCookie('user', JSON.stringify(payload.data));
            router.push('/');
          } else if (response.status == 400) {
            toast.error('Email already exists');
          } else {
            toast.error('Error when login user');
          }
        });
      } else if (response.status == 400) {
        toast.error('Email already exists');
      } else {
        toast.error('Error when creating user');
      }
    });
  }
  if (isLoading)
    return (
      <div className="w-full flex h-full items-center justify-center">
        <Loader />
      </div>
    );
  return (
    <div className="w-full flex flex-col items-center justify-center">
      <div
        className={cn('grid gap-6 w-[80%] md:w-[70%] lg:w-[60%] ', className)}
      >
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)}>
            <div className="grid gap-6">
              <div className="gap-8 flex flex-col">
                <div className="flex flex-col gap-3 ">
                  <Label className="font-bold">Email</Label>
                  <FormField
                    name="email"
                    control={form.control}
                    render={({ field }) => (
                      <FormItem>
                        <FormControl>
                          <Input
                            className="text-slate-500"
                            type="email"
                            placeholder="Enter your email"
                            autoComplete="username"
                            {...field}
                          />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>
                <div className="flex flex-col gap-3 ">
                  <Label className="font-bold">Username</Label>
                  <FormField
                    control={form.control}
                    name="username"
                    render={({ field }) => (
                      <FormItem>
                        <FormControl>
                          <Input
                            className="text-slate-500"
                            type="text"
                            placeholder="Enter your username"
                            {...field}
                          />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>
                <div className="flex flex-col gap-3 ">
                  <Label className="font-bold">Password</Label>
                  <FormField
                    control={form.control}
                    name="password"
                    render={({ field }) => {
                      return (
                        <FormItem>
                          <FormControl>
                            <Input
                              className="text-slate-500"
                              placeholder="Enter your password"
                              type={show.password ? 'text' : 'password'}
                              value={field.value}
                              onChange={field.onChange}
                              renderRight={
                                <div
                                  onClick={() => {
                                    setShow({
                                      ...show,
                                      password: !show.password,
                                    });
                                  }}
                                  className="opacity-50 cursor-pointer hover:opacity-100"
                                >
                                  {show.password ? (
                                    <AiFillEyeInvisible size={20} />
                                  ) : (
                                    <AiFillEye size={20} />
                                  )}
                                </div>
                              }
                            />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      );
                    }}
                  />
                </div>
                <div className="flex flex-col gap-3 ">
                  <Label className="font-bold">Confirm password</Label>
                  <FormField
                    control={form.control}
                    name="confirmPassword"
                    render={({ field }) => {
                      return (
                        <FormItem>
                          <FormControl>
                            <Input
                              className="text-slate-500"
                              placeholder="Confirm your password"
                              type={show.confirmPassword ? 'text' : 'password'}
                              value={field.value}
                              onChange={field.onChange}
                              renderRight={
                                <div
                                  onClick={() => {
                                    setShow({
                                      ...show,
                                      confirmPassword: !show.confirmPassword,
                                    });
                                  }}
                                  className="opacity-50 cursor-pointer hover:opacity-100"
                                >
                                  {show.confirmPassword ? (
                                    <AiFillEyeInvisible size={20} />
                                  ) : (
                                    <AiFillEye size={20} />
                                  )}
                                </div>
                              }
                            />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      );
                    }}
                  />
                </div>
              </div>

              <Button type="submit" className="">
                Sign Up
              </Button>
            </div>
          </form>
        </Form>
      </div>
      <p className=" mt-10 text-center text-sm text-muted-foreground">
        Already have an account?{' '}
        <Link className=" font-bold underline text-black" href="/login">
          Sign In
        </Link>
      </p>
    </div>
  );
};

export default Register;

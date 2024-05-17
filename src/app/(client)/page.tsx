'use client';
import { isSessionValid } from '@/lib/auth';
import RecommendPage from './recommend/RecommendPage';
import { useRouter } from 'next/navigation';
import Cookies from 'js-cookie';
import jwt from 'jsonwebtoken';
import { useEffect } from 'react';

export default function Home() {
  const router = useRouter();

  if (!isSessionValid()) {
    router.push('/login');
  }

  return (
    <div className="w-full h-full bg-white">
      <RecommendPage></RecommendPage>
    </div>
  );
}

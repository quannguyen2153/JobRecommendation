'use client';
import { isSessionValid } from '@/lib/auth';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';
import RecommendPage from './RecommendPage';

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    if (!isSessionValid()) {
      router.push('/login');
    }
  }, []);

  return <RecommendPage />;
}

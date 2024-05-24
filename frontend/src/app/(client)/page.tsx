'use client';
import { isSessionValid } from '@/lib/auth';
import RecommendPage from './recommend/RecommendPage';
import { useRouter } from 'next/navigation';
import Cookies from 'js-cookie';
import jwt from 'jsonwebtoken';
import { useEffect } from 'react';

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    if (!isSessionValid()) {
      router.push('/login');
    }
  }, []);

  const url =
    'https://public.tableau.com/views/bootcamp_17161932669370/JobInsights?:showVizHome=no&:embed=true';
  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
      }}
    >
      <iframe title="Tableau Dashboard" width="80%" height="100%" src={url} />
    </div>
  );
}

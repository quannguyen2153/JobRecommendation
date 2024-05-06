'use client';
import React, { useState } from 'react';
import {
  Navbar,
  NavbarBrand,
  NavbarContent,
  NavbarItem,
  Link,
  Button,
} from '@nextui-org/react';
import { Constants } from '@/lib/constants';
import { AssetSvg } from '@/assets/AssetSvg';
import { usePathname, useRouter } from 'next/navigation';

export default function App() {
  const router = useRouter(); // Using Next.js Router
  const pathname = usePathname(); //Gewt the current path
  const handleClick = (path: string) => {
    router.push(path); // Use client-side routing
  };
  return (
    <Navbar position="sticky" className="w-full justify-evenly bg-secondary">
      <NavbarBrand>
        {AssetSvg.logo()}
        <p className="font-bold text-primary">{Constants.APP_NAME}</p>
      </NavbarBrand>
      <NavbarContent className="hidden sm:flex gap-4" justify="center">
        <NavbarItem className={`${pathname === '/' ? 'font-bold' : ''}`}>
          <Link color="foreground" href="/" onClick={() => handleClick('/')}>
            Home
          </Link>
        </NavbarItem>
        <NavbarItem className={`${pathname === '/search' ? 'font-bold' : ''}`}>
          <Link
            href="/search"
            aria-current="page"
            onClick={() => handleClick('/search')}
          >
            Search
          </Link>
        </NavbarItem>
        <NavbarItem
          className={`${pathname === '/recommend' ? 'font-bold' : ''}`}
        >
          <Link
            color="foreground"
            href="/recommend"
            onClick={() => handleClick('/recommend')}
          >
            Recommendation
          </Link>
        </NavbarItem>
        <NavbarItem
          className={`${pathname === '/improve-cv' ? 'font-bold' : ''}`}
        >
          <Link
            color="foreground"
            href="/improve-cv"
            onClick={() => handleClick('/improve-cv')}
          >
            Improve your CV
          </Link>
        </NavbarItem>
      </NavbarContent>
      <NavbarContent justify="end">
        <NavbarItem className="hidden lg:flex">
          <Link href="#">Login</Link>
        </NavbarItem>
        <NavbarItem>
          <Button as={Link} color="primary" href="#" variant="solid">
            Sign Up
          </Button>
        </NavbarItem>
      </NavbarContent>
    </Navbar>
  );
}

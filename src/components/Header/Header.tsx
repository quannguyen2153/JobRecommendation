'use client';

import {
  Navbar,
  NavbarBrand,
  NavbarContent,
  NavbarItem,
  Link,
  Button,
  Dropdown,
  DropdownTrigger,
  DropdownItem,
  DropdownMenu,
  Avatar,
} from '@nextui-org/react';
import React, { useEffect, useState } from 'react';
import { Constants } from '@/lib/constants';
import { AssetSvg } from '@/assets/AssetSvg';
import { usePathname, useRouter } from 'next/navigation';
import Image from 'next/image';
import { useUser } from '@/hooks/useUser';
import { deleteCookie, getCookie } from 'cookies-next';

export const Header = () => {
  const [user, setUser] = useState<string | null>(null);
  const [avatar, setAvatar] = useState(null);

  const { onGetAvatar } = useUser();

  useEffect(() => {
    if (typeof window !== 'undefined' && getCookie('user')) {
      setUser(JSON.parse(getCookie('user')!));
      onGetAvatar((response: any) => {
        console.log('🚀 ~ response:', response);
        if (response.status === 200) {
          setAvatar(response.data);
        }
      });
    }
  }, []);

  const router = useRouter(); // Using Next.js Router
  const pathname = usePathname(); //Gewt the current path
  const handleClick = (path: string) => {
    router.push(path); // Use client-side routing
  };

  const handleLogout = () => {
    deleteCookie('token');
    deleteCookie('user');
    router.push('/login'); // Redirect to login page
  };
  return (
    <Navbar position="sticky" className="w-full justify-evenly bg-secondary">
      <NavbarBrand>
        {AssetSvg.logo()}
        <p className="font-bold text-primary">{Constants.APP_NAME}</p>
      </NavbarBrand>

      <NavbarContent justify="center">
        <NavbarItem className="hidden lg:flex">
          <Link href="/">Home</Link>
        </NavbarItem>
        <NavbarItem className="hidden lg:flex">
          <Link href="/dashboard">Dashboard</Link>
        </NavbarItem>
      </NavbarContent>

      {user ? (
        <NavbarContent justify="end" className="w-32">
          <Dropdown placement="bottom-end" className="text-black">
            <DropdownTrigger>
              <Button
                isIconOnly
                color="primary"
                variant="bordered"
                size="md"
                radius="full"
                startContent={
                  avatar ? (
                    <div
                      style={{
                        width: '70px',
                        height: '70px',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                      }}
                      dangerouslySetInnerHTML={{ __html: avatar }}
                    />
                  ) : (
                    AssetSvg.human()
                  )
                }
              ></Button>
            </DropdownTrigger>
            <DropdownMenu aria-label="Profile Actions" variant="flat">
              <DropdownItem key="profile" className="h-14 gap-2">
                <p className="font-semibold">{user!!.email}</p>
              </DropdownItem>
              <DropdownItem key="help_and_feedback">Profile</DropdownItem>
              <DropdownItem key="logout" color="danger" onClick={handleLogout}>
                <p className="font-bold text-red-600">Log Out</p>
              </DropdownItem>
            </DropdownMenu>
          </Dropdown>
        </NavbarContent>
      ) : (
        <NavbarContent justify="end">
          <NavbarItem className="hidden lg:flex">
            <Link href="/login">Login</Link>
          </NavbarItem>
          <NavbarItem>
            <Button as={Link} color="primary" href="/register" variant="solid">
              Sign Up
            </Button>
          </NavbarItem>
        </NavbarContent>
      )}
      {/* <NavbarContent justify="end" className="w-32">
        <Dropdown placement="bottom-end" className="text-black">
          <DropdownTrigger>
            <Button
              isIconOnly
              color="primary"
              variant="bordered"
              size="md"
              radius="full"
              startContent={AssetSvg.human()}
            ></Button>
          </DropdownTrigger>
          <DropdownMenu aria-label="Profile Actions" variant="flat">
            <DropdownItem key="profile" className="h-14 gap-2">
              <p className="font-semibold">zoey@example.com</p>
            </DropdownItem>
            <DropdownItem key="help_and_feedback">Profile</DropdownItem>
            <DropdownItem key="logout" color="danger">
              Log Out
            </DropdownItem>
          </DropdownMenu>
        </Dropdown>
      </NavbarContent> */}
    </Navbar>
  );
};

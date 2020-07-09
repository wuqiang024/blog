#! /usr/bin/env python3
# -*- encoding:utf-8 -*-
import asyncio

async def heelo():
    print('hello')
    r = await asyncio.sleep(10)
    print('world')

heelo()
#!/usr/bin/env python
"""

Copyright (c) 2016-2018 Alex Forencich

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

from myhdl import *
import os

import axis_ep

module = 'axis_switch_4x4'
testbench = 'test_%s_64' % module

srcs = []

srcs.append("../rtl/%s.v" % module)
srcs.append("../rtl/arbiter.v")
srcs.append("../rtl/priority_encoder.v")
srcs.append("%s.v" % testbench)

src = ' '.join(srcs)

build_cmd = "iverilog -o %s.vvp %s" % (testbench, src)

def bench():

    # Parameters
    DATA_WIDTH = 64
    KEEP_ENABLE = (DATA_WIDTH>8)
    KEEP_WIDTH = (DATA_WIDTH/8)
    ID_ENABLE = 1
    ID_WIDTH = 8
    DEST_WIDTH = 3
    USER_ENABLE = 1
    USER_WIDTH = 1
    OUT_0_BASE = 0
    OUT_0_TOP = 0
    OUT_0_CONNECT = 0xf
    OUT_1_BASE = 1
    OUT_1_TOP = 1
    OUT_1_CONNECT = 0xf
    OUT_2_BASE = 2
    OUT_2_TOP = 2
    OUT_2_CONNECT = 0xf
    OUT_3_BASE = 3
    OUT_3_TOP = 3
    OUT_3_CONNECT = 0xf
    ARB_TYPE = "ROUND_ROBIN"
    LSB_PRIORITY = "HIGH"

    # Inputs
    clk = Signal(bool(0))
    rst = Signal(bool(0))
    current_test = Signal(intbv(0)[8:])

    input_0_axis_tdata = Signal(intbv(0)[DATA_WIDTH:])
    input_0_axis_tkeep = Signal(intbv(1)[KEEP_WIDTH:])
    input_0_axis_tvalid = Signal(bool(0))
    input_0_axis_tlast = Signal(bool(0))
    input_0_axis_tid = Signal(intbv(0)[ID_WIDTH:])
    input_0_axis_tdest = Signal(intbv(0)[DEST_WIDTH:])
    input_0_axis_tuser = Signal(intbv(0)[USER_WIDTH:])
    input_1_axis_tdata = Signal(intbv(0)[DATA_WIDTH:])
    input_1_axis_tkeep = Signal(intbv(1)[KEEP_WIDTH:])
    input_1_axis_tvalid = Signal(bool(0))
    input_1_axis_tlast = Signal(bool(0))
    input_1_axis_tid = Signal(intbv(0)[ID_WIDTH:])
    input_1_axis_tdest = Signal(intbv(0)[DEST_WIDTH:])
    input_1_axis_tuser = Signal(intbv(0)[USER_WIDTH:])
    input_2_axis_tdata = Signal(intbv(0)[DATA_WIDTH:])
    input_2_axis_tkeep = Signal(intbv(1)[KEEP_WIDTH:])
    input_2_axis_tvalid = Signal(bool(0))
    input_2_axis_tlast = Signal(bool(0))
    input_2_axis_tid = Signal(intbv(0)[ID_WIDTH:])
    input_2_axis_tdest = Signal(intbv(0)[DEST_WIDTH:])
    input_2_axis_tuser = Signal(intbv(0)[USER_WIDTH:])
    input_3_axis_tdata = Signal(intbv(0)[DATA_WIDTH:])
    input_3_axis_tkeep = Signal(intbv(1)[KEEP_WIDTH:])
    input_3_axis_tvalid = Signal(bool(0))
    input_3_axis_tlast = Signal(bool(0))
    input_3_axis_tid = Signal(intbv(0)[ID_WIDTH:])
    input_3_axis_tdest = Signal(intbv(0)[DEST_WIDTH:])
    input_3_axis_tuser = Signal(intbv(0)[USER_WIDTH:])
    output_0_axis_tready = Signal(bool(0))
    output_1_axis_tready = Signal(bool(0))
    output_2_axis_tready = Signal(bool(0))
    output_3_axis_tready = Signal(bool(0))

    # Outputs
    input_0_axis_tready = Signal(bool(0))
    input_1_axis_tready = Signal(bool(0))
    input_2_axis_tready = Signal(bool(0))
    input_3_axis_tready = Signal(bool(0))
    output_0_axis_tdata = Signal(intbv(0)[DATA_WIDTH:])
    output_0_axis_tkeep = Signal(intbv(1)[KEEP_WIDTH:])
    output_0_axis_tvalid = Signal(bool(0))
    output_0_axis_tlast = Signal(bool(0))
    output_0_axis_tid = Signal(intbv(0)[ID_WIDTH:])
    output_0_axis_tdest = Signal(intbv(0)[DEST_WIDTH:])
    output_0_axis_tuser = Signal(intbv(0)[USER_WIDTH:])
    output_1_axis_tdata = Signal(intbv(0)[DATA_WIDTH:])
    output_1_axis_tkeep = Signal(intbv(1)[KEEP_WIDTH:])
    output_1_axis_tvalid = Signal(bool(0))
    output_1_axis_tlast = Signal(bool(0))
    output_1_axis_tid = Signal(intbv(0)[ID_WIDTH:])
    output_1_axis_tdest = Signal(intbv(0)[DEST_WIDTH:])
    output_1_axis_tuser = Signal(intbv(0)[USER_WIDTH:])
    output_2_axis_tdata = Signal(intbv(0)[DATA_WIDTH:])
    output_2_axis_tkeep = Signal(intbv(1)[KEEP_WIDTH:])
    output_2_axis_tvalid = Signal(bool(0))
    output_2_axis_tlast = Signal(bool(0))
    output_2_axis_tid = Signal(intbv(0)[ID_WIDTH:])
    output_2_axis_tdest = Signal(intbv(0)[DEST_WIDTH:])
    output_2_axis_tuser = Signal(intbv(0)[USER_WIDTH:])
    output_3_axis_tdata = Signal(intbv(0)[DATA_WIDTH:])
    output_3_axis_tkeep = Signal(intbv(1)[KEEP_WIDTH:])
    output_3_axis_tvalid = Signal(bool(0))
    output_3_axis_tlast = Signal(bool(0))
    output_3_axis_tid = Signal(intbv(0)[ID_WIDTH:])
    output_3_axis_tdest = Signal(intbv(0)[DEST_WIDTH:])
    output_3_axis_tuser = Signal(intbv(0)[USER_WIDTH:])

    # sources and sinks
    source_0_pause = Signal(bool(0))
    source_1_pause = Signal(bool(0))
    source_2_pause = Signal(bool(0))
    source_3_pause = Signal(bool(0))
    sink_0_pause = Signal(bool(0))
    sink_1_pause = Signal(bool(0))
    sink_2_pause = Signal(bool(0))
    sink_3_pause = Signal(bool(0))

    source_0 = axis_ep.AXIStreamSource()

    source_0_logic = source_0.create_logic(
        clk,
        rst,
        tdata=input_0_axis_tdata,
        tkeep=input_0_axis_tkeep,
        tvalid=input_0_axis_tvalid,
        tready=input_0_axis_tready,
        tlast=input_0_axis_tlast,
        tid=input_0_axis_tid,
        tdest=input_0_axis_tdest,
        tuser=input_0_axis_tuser,
        pause=source_0_pause,
        name='source_0'
    )

    source_1 = axis_ep.AXIStreamSource()

    source_1_logic = source_1.create_logic(
        clk,
        rst,
        tdata=input_1_axis_tdata,
        tkeep=input_1_axis_tkeep,
        tvalid=input_1_axis_tvalid,
        tready=input_1_axis_tready,
        tlast=input_1_axis_tlast,
        tid=input_1_axis_tid,
        tdest=input_1_axis_tdest,
        tuser=input_1_axis_tuser,
        pause=source_1_pause,
        name='source_1'
    )

    source_2 = axis_ep.AXIStreamSource()

    source_2_logic = source_2.create_logic(
        clk,
        rst,
        tdata=input_2_axis_tdata,
        tkeep=input_2_axis_tkeep,
        tvalid=input_2_axis_tvalid,
        tready=input_2_axis_tready,
        tlast=input_2_axis_tlast,
        tid=input_2_axis_tid,
        tdest=input_2_axis_tdest,
        tuser=input_2_axis_tuser,
        pause=source_2_pause,
        name='source_2'
    )

    source_3 = axis_ep.AXIStreamSource()

    source_3_logic = source_3.create_logic(
        clk,
        rst,
        tdata=input_3_axis_tdata,
        tkeep=input_3_axis_tkeep,
        tvalid=input_3_axis_tvalid,
        tready=input_3_axis_tready,
        tlast=input_3_axis_tlast,
        tid=input_3_axis_tid,
        tdest=input_3_axis_tdest,
        tuser=input_3_axis_tuser,
        pause=source_3_pause,
        name='source_3'
    )

    sink_0 = axis_ep.AXIStreamSink()

    sink_0_logic = sink_0.create_logic(
        clk,
        rst,
        tdata=output_0_axis_tdata,
        tkeep=output_0_axis_tkeep,
        tvalid=output_0_axis_tvalid,
        tready=output_0_axis_tready,
        tlast=output_0_axis_tlast,
        tid=output_0_axis_tid,
        tdest=output_0_axis_tdest,
        tuser=output_0_axis_tuser,
        pause=sink_0_pause,
        name='sink_0'
    )

    sink_1 = axis_ep.AXIStreamSink()

    sink_1_logic = sink_1.create_logic(
        clk,
        rst,
        tdata=output_1_axis_tdata,
        tkeep=output_1_axis_tkeep,
        tvalid=output_1_axis_tvalid,
        tready=output_1_axis_tready,
        tlast=output_1_axis_tlast,
        tid=output_1_axis_tid,
        tdest=output_1_axis_tdest,
        tuser=output_1_axis_tuser,
        pause=sink_1_pause,
        name='sink_1'
    )

    sink_2 = axis_ep.AXIStreamSink()

    sink_2_logic = sink_2.create_logic(
        clk,
        rst,
        tdata=output_2_axis_tdata,
        tkeep=output_2_axis_tkeep,
        tvalid=output_2_axis_tvalid,
        tready=output_2_axis_tready,
        tlast=output_2_axis_tlast,
        tid=output_2_axis_tid,
        tdest=output_2_axis_tdest,
        tuser=output_2_axis_tuser,
        pause=sink_2_pause,
        name='sink_2'
    )

    sink_3 = axis_ep.AXIStreamSink()

    sink_3_logic = sink_3.create_logic(
        clk,
        rst,
        tdata=output_3_axis_tdata,
        tkeep=output_3_axis_tkeep,
        tvalid=output_3_axis_tvalid,
        tready=output_3_axis_tready,
        tlast=output_3_axis_tlast,
        tid=output_3_axis_tid,
        tdest=output_3_axis_tdest,
        tuser=output_3_axis_tuser,
        pause=sink_3_pause,
        name='sink_3'
    )

    # DUT
    if os.system(build_cmd):
        raise Exception("Error running build command")

    dut = Cosimulation(
        "vvp -m myhdl %s.vvp -lxt2" % testbench,
        clk=clk,
        rst=rst,
        current_test=current_test,

        input_0_axis_tdata=input_0_axis_tdata,
        input_0_axis_tkeep=input_0_axis_tkeep,
        input_0_axis_tvalid=input_0_axis_tvalid,
        input_0_axis_tready=input_0_axis_tready,
        input_0_axis_tlast=input_0_axis_tlast,
        input_0_axis_tid=input_0_axis_tid,
        input_0_axis_tdest=input_0_axis_tdest,
        input_0_axis_tuser=input_0_axis_tuser,
        input_1_axis_tdata=input_1_axis_tdata,
        input_1_axis_tkeep=input_1_axis_tkeep,
        input_1_axis_tvalid=input_1_axis_tvalid,
        input_1_axis_tready=input_1_axis_tready,
        input_1_axis_tlast=input_1_axis_tlast,
        input_1_axis_tid=input_1_axis_tid,
        input_1_axis_tdest=input_1_axis_tdest,
        input_1_axis_tuser=input_1_axis_tuser,
        input_2_axis_tdata=input_2_axis_tdata,
        input_2_axis_tkeep=input_2_axis_tkeep,
        input_2_axis_tvalid=input_2_axis_tvalid,
        input_2_axis_tready=input_2_axis_tready,
        input_2_axis_tlast=input_2_axis_tlast,
        input_2_axis_tid=input_2_axis_tid,
        input_2_axis_tdest=input_2_axis_tdest,
        input_2_axis_tuser=input_2_axis_tuser,
        input_3_axis_tdata=input_3_axis_tdata,
        input_3_axis_tkeep=input_3_axis_tkeep,
        input_3_axis_tvalid=input_3_axis_tvalid,
        input_3_axis_tready=input_3_axis_tready,
        input_3_axis_tlast=input_3_axis_tlast,
        input_3_axis_tid=input_3_axis_tid,
        input_3_axis_tdest=input_3_axis_tdest,
        input_3_axis_tuser=input_3_axis_tuser,

        output_0_axis_tdata=output_0_axis_tdata,
        output_0_axis_tkeep=output_0_axis_tkeep,
        output_0_axis_tvalid=output_0_axis_tvalid,
        output_0_axis_tready=output_0_axis_tready,
        output_0_axis_tlast=output_0_axis_tlast,
        output_0_axis_tid=output_0_axis_tid,
        output_0_axis_tdest=output_0_axis_tdest,
        output_0_axis_tuser=output_0_axis_tuser,
        output_1_axis_tdata=output_1_axis_tdata,
        output_1_axis_tkeep=output_1_axis_tkeep,
        output_1_axis_tvalid=output_1_axis_tvalid,
        output_1_axis_tready=output_1_axis_tready,
        output_1_axis_tlast=output_1_axis_tlast,
        output_1_axis_tid=output_1_axis_tid,
        output_1_axis_tdest=output_1_axis_tdest,
        output_1_axis_tuser=output_1_axis_tuser,
        output_2_axis_tdata=output_2_axis_tdata,
        output_2_axis_tkeep=output_2_axis_tkeep,
        output_2_axis_tvalid=output_2_axis_tvalid,
        output_2_axis_tready=output_2_axis_tready,
        output_2_axis_tlast=output_2_axis_tlast,
        output_2_axis_tid=output_2_axis_tid,
        output_2_axis_tdest=output_2_axis_tdest,
        output_2_axis_tuser=output_2_axis_tuser,
        output_3_axis_tdata=output_3_axis_tdata,
        output_3_axis_tkeep=output_3_axis_tkeep,
        output_3_axis_tvalid=output_3_axis_tvalid,
        output_3_axis_tready=output_3_axis_tready,
        output_3_axis_tlast=output_3_axis_tlast,
        output_3_axis_tid=output_3_axis_tid,
        output_3_axis_tdest=output_3_axis_tdest,
        output_3_axis_tuser=output_3_axis_tuser
    )

    @always(delay(4))
    def clkgen():
        clk.next = not clk

    def wait_normal():
        while input_0_axis_tvalid or input_1_axis_tvalid or input_2_axis_tvalid or input_3_axis_tvalid:
            yield clk.posedge

    def wait_pause_source():
        while input_0_axis_tvalid or input_1_axis_tvalid or input_2_axis_tvalid or input_3_axis_tvalid:
            source_0_pause.next = True
            source_1_pause.next = True
            source_2_pause.next = True
            source_3_pause.next = True
            yield clk.posedge
            yield clk.posedge
            yield clk.posedge
            source_0_pause.next = False
            source_1_pause.next = False
            source_2_pause.next = False
            source_3_pause.next = False
            yield clk.posedge

    def wait_pause_sink():
        while input_0_axis_tvalid or input_1_axis_tvalid or input_2_axis_tvalid or input_3_axis_tvalid:
            sink_0_pause.next = True
            sink_1_pause.next = True
            sink_2_pause.next = True
            sink_3_pause.next = True
            yield clk.posedge
            yield clk.posedge
            yield clk.posedge
            sink_0_pause.next = False
            sink_1_pause.next = False
            sink_2_pause.next = False
            sink_3_pause.next = False
            yield clk.posedge

    @instance
    def check():
        yield delay(100)
        yield clk.posedge
        rst.next = 1
        yield clk.posedge
        rst.next = 0
        yield clk.posedge
        yield delay(100)
        yield clk.posedge

        # testbench stimulus

        yield clk.posedge
        print("test 1: 0123 -> 0123")
        current_test.next = 1

        test_frame0 = axis_ep.AXIStreamFrame(b'\x01\x00\x00\xFF\x01\x02\x03\x04\x05\x06\x07\x08', id=0, dest=0)
        test_frame1 = axis_ep.AXIStreamFrame(b'\x01\x01\x01\xFF\x01\x02\x03\x04\x05\x06\x07\x08', id=1, dest=1)
        test_frame2 = axis_ep.AXIStreamFrame(b'\x01\x02\x02\xFF\x01\x02\x03\x04\x05\x06\x07\x08', id=2, dest=2)
        test_frame3 = axis_ep.AXIStreamFrame(b'\x01\x03\x03\xFF\x01\x02\x03\x04\x05\x06\x07\x08', id=3, dest=3)

        for wait in wait_normal, wait_pause_source, wait_pause_sink:
            source_0.send(test_frame0)
            source_1.send(test_frame1)
            source_2.send(test_frame2)
            source_3.send(test_frame3)
            yield clk.posedge
            yield clk.posedge

            yield wait()

            yield sink_0.wait()
            rx_frame0 = sink_0.recv()

            assert rx_frame0 == test_frame0

            yield sink_1.wait()
            rx_frame1 = sink_1.recv()

            assert rx_frame1 == test_frame1

            yield sink_2.wait()
            rx_frame2 = sink_2.recv()

            assert rx_frame2 == test_frame2

            yield sink_3.wait()
            rx_frame3 = sink_3.recv()

            assert rx_frame3 == test_frame3

            yield delay(100)

        yield clk.posedge
        print("test 2: 0123 -> 3210")
        current_test.next = 2

        test_frame0 = axis_ep.AXIStreamFrame(b'\x02\x00\x03\xFF\x01\x02\x03\x04\x05\x06\x07\x08', id=0, dest=3)
        test_frame1 = axis_ep.AXIStreamFrame(b'\x02\x01\x02\xFF\x01\x02\x03\x04\x05\x06\x07\x08', id=1, dest=2)
        test_frame2 = axis_ep.AXIStreamFrame(b'\x02\x02\x01\xFF\x01\x02\x03\x04\x05\x06\x07\x08', id=2, dest=1)
        test_frame3 = axis_ep.AXIStreamFrame(b'\x02\x03\x00\xFF\x01\x02\x03\x04\x05\x06\x07\x08', id=3, dest=0)

        for wait in wait_normal, wait_pause_source, wait_pause_sink:
            source_0.send(test_frame0)
            source_1.send(test_frame1)
            source_2.send(test_frame2)
            source_3.send(test_frame3)
            yield clk.posedge
            yield clk.posedge

            yield wait()

            yield sink_0.wait()
            rx_frame0 = sink_0.recv()

            assert rx_frame0 == test_frame3

            yield sink_1.wait()
            rx_frame1 = sink_1.recv()

            assert rx_frame1 == test_frame2

            yield sink_2.wait()
            rx_frame2 = sink_2.recv()

            assert rx_frame2 == test_frame1

            yield sink_3.wait()
            rx_frame3 = sink_3.recv()

            assert rx_frame3 == test_frame0

            yield delay(100)

        yield clk.posedge
        print("test 3: 0000 -> 0123")
        current_test.next = 3

        test_frame0 = axis_ep.AXIStreamFrame(b'\x02\x00\x00\xFF\x01\x02\x03\x04\x05\x06\x07\x08', id=0, dest=0)
        test_frame1 = axis_ep.AXIStreamFrame(b'\x02\x00\x01\xFF\x01\x02\x03\x04\x05\x06\x07\x08', id=0, dest=1)
        test_frame2 = axis_ep.AXIStreamFrame(b'\x02\x00\x02\xFF\x01\x02\x03\x04\x05\x06\x07\x08', id=0, dest=2)
        test_frame3 = axis_ep.AXIStreamFrame(b'\x02\x00\x03\xFF\x01\x02\x03\x04\x05\x06\x07\x08', id=0, dest=3)

        for wait in wait_normal, wait_pause_source, wait_pause_sink:
            source_0.send(test_frame0)
            source_0.send(test_frame1)
            source_0.send(test_frame2)
            source_0.send(test_frame3)
            yield clk.posedge
            yield clk.posedge

            yield wait()

            yield sink_0.wait()
            rx_frame0 = sink_0.recv()

            assert rx_frame0 == test_frame0

            yield sink_1.wait()
            rx_frame1 = sink_1.recv()

            assert rx_frame1 == test_frame1

            yield sink_2.wait()
            rx_frame2 = sink_2.recv()

            assert rx_frame2 == test_frame2

            yield sink_3.wait()
            rx_frame3 = sink_3.recv()

            assert rx_frame3 == test_frame3

            yield delay(100)

        yield clk.posedge
        print("test 4: 0123 -> 0000")
        current_test.next = 4

        test_frame0 = axis_ep.AXIStreamFrame(b'\x02\x00\x00\xFF\x01\x02\x03\x04\x05\x06\x07\x08', id=0, dest=0)
        test_frame1 = axis_ep.AXIStreamFrame(b'\x02\x01\x00\xFF\x01\x02\x03\x04\x05\x06\x07\x08', id=1, dest=0)
        test_frame2 = axis_ep.AXIStreamFrame(b'\x02\x02\x00\xFF\x01\x02\x03\x04\x05\x06\x07\x08', id=2, dest=0)
        test_frame3 = axis_ep.AXIStreamFrame(b'\x02\x03\x00\xFF\x01\x02\x03\x04\x05\x06\x07\x08', id=3, dest=0)

        for wait in wait_normal, wait_pause_source, wait_pause_sink:
            source_0.send(test_frame0)
            yield clk.posedge
            source_1.send(test_frame1)
            source_2.send(test_frame2)
            source_3.send(test_frame3)
            yield clk.posedge

            yield wait()

            yield sink_0.wait()
            rx_frame0 = sink_0.recv()

            assert rx_frame0 == test_frame0

            yield sink_0.wait()
            rx_frame1 = sink_0.recv()

            assert rx_frame1 == test_frame1

            yield sink_0.wait()
            rx_frame2 = sink_0.recv()

            assert rx_frame2 == test_frame2

            yield sink_0.wait()
            rx_frame3 = sink_0.recv()

            assert rx_frame3 == test_frame3

            yield delay(100)

        yield clk.posedge
        print("test 1: bad decoding")
        current_test.next = 1

        test_frame0 = axis_ep.AXIStreamFrame(b'\x01\x00\x00\xFF\x01\x02\x03\x04\x05\x06\x07\x08', id=0, dest=0)
        test_frame1 = axis_ep.AXIStreamFrame(b'\x01\x01\x01\xFF\x01\x02\x03\x04\x05\x06\x07\x08', id=1, dest=1)
        test_frame2 = axis_ep.AXIStreamFrame(b'\x01\x02\x04\xFF\x01\x02\x03\x04\x05\x06\x07\x08', id=2, dest=4)
        test_frame3 = axis_ep.AXIStreamFrame(b'\x01\x03\x05\xFF\x01\x02\x03\x04\x05\x06\x07\x08', id=3, dest=5)

        for wait in wait_normal, wait_pause_source, wait_pause_sink:
            source_0.send(test_frame0)
            source_1.send(test_frame1)
            source_2.send(test_frame2)
            source_3.send(test_frame3)
            yield clk.posedge
            yield clk.posedge

            yield wait()

            yield sink_0.wait()
            rx_frame0 = sink_0.recv()

            assert rx_frame0 == test_frame0

            yield sink_1.wait()
            rx_frame1 = sink_1.recv()

            assert rx_frame1 == test_frame1

            yield delay(100)

        raise StopSimulation

    return instances()

def test_bench():
    sim = Simulation(bench())
    sim.run()

if __name__ == '__main__':
    print("Running test...")
    test_bench()

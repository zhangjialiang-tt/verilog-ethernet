#!/usr/bin/env python2
"""

Copyright (c) 2014 Alex Forencich

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
from Queue import Queue

import arp_ep
import eth_ep

module = 'arp_eth_rx_64'

srcs = []

srcs.append("../rtl/%s.v" % module)
srcs.append("test_%s.v" % module)

src = ' '.join(srcs)

build_cmd = "iverilog -o test_%s.vvp %s" % (module, src)

def dut_arp_eth_rx_64(clk,
                    rst,
                    current_test,

                    input_eth_hdr_valid,
                    input_eth_hdr_ready,
                    input_eth_dest_mac,
                    input_eth_src_mac,
                    input_eth_type,
                    input_eth_payload_tdata,
                    input_eth_payload_tkeep,
                    input_eth_payload_tvalid,
                    input_eth_payload_tready,
                    input_eth_payload_tlast,
                    input_eth_payload_tuser,

                    output_frame_valid,
                    output_frame_ready,
                    output_eth_dest_mac,
                    output_eth_src_mac,
                    output_eth_type,
                    output_arp_htype,
                    output_arp_ptype,
                    output_arp_hlen,
                    output_arp_plen,
                    output_arp_oper,
                    output_arp_sha,
                    output_arp_spa,
                    output_arp_tha,
                    output_arp_tpa,

                    busy,
                    error_header_early_termination):

    if os.system(build_cmd):
        raise Exception("Error running build command")
    return Cosimulation("vvp -m myhdl test_%s.vvp -lxt2" % module,
                clk=clk,
                rst=rst,
                current_test=current_test,

                input_eth_hdr_valid=input_eth_hdr_valid,
                input_eth_hdr_ready=input_eth_hdr_ready,
                input_eth_dest_mac=input_eth_dest_mac,
                input_eth_src_mac=input_eth_src_mac,
                input_eth_type=input_eth_type,
                input_eth_payload_tdata=input_eth_payload_tdata,
                input_eth_payload_tkeep=input_eth_payload_tkeep,
                input_eth_payload_tvalid=input_eth_payload_tvalid,
                input_eth_payload_tready=input_eth_payload_tready,
                input_eth_payload_tlast=input_eth_payload_tlast,
                input_eth_payload_tuser=input_eth_payload_tuser,

                output_frame_valid=output_frame_valid,
                output_frame_ready=output_frame_ready,
                output_eth_dest_mac=output_eth_dest_mac,
                output_eth_src_mac=output_eth_src_mac,
                output_eth_type=output_eth_type,
                output_arp_htype=output_arp_htype,
                output_arp_ptype=output_arp_ptype,
                output_arp_hlen=output_arp_hlen,
                output_arp_plen=output_arp_plen,
                output_arp_oper=output_arp_oper,
                output_arp_sha=output_arp_sha,
                output_arp_spa=output_arp_spa,
                output_arp_tha=output_arp_tha,
                output_arp_tpa=output_arp_tpa,

                busy=busy,
                error_header_early_termination=error_header_early_termination)

def bench():

    # Inputs
    clk = Signal(bool(0))
    rst = Signal(bool(0))
    current_test = Signal(intbv(0)[8:])

    input_eth_hdr_valid = Signal(bool(0))
    input_eth_dest_mac = Signal(intbv(0)[48:])
    input_eth_src_mac = Signal(intbv(0)[48:])
    input_eth_type = Signal(intbv(0)[16:])
    input_eth_payload_tdata = Signal(intbv(0)[64:])
    input_eth_payload_tkeep = Signal(intbv(0)[8:])
    input_eth_payload_tvalid = Signal(bool(0))
    input_eth_payload_tlast = Signal(bool(0))
    input_eth_payload_tuser = Signal(bool(0))
    output_frame_ready = Signal(bool(0))

    # Outputs
    input_eth_hdr_ready = Signal(bool(0))
    input_eth_payload_tready = Signal(bool(0))
    output_frame_valid = Signal(bool(0))
    output_eth_dest_mac = Signal(intbv(0)[48:])
    output_eth_src_mac = Signal(intbv(0)[48:])
    output_eth_type = Signal(intbv(0)[16:])
    output_arp_htype = Signal(intbv(0)[16:])
    output_arp_ptype = Signal(intbv(0)[16:])
    output_arp_hlen = Signal(intbv(0)[8:])
    output_arp_plen = Signal(intbv(0)[8:])
    output_arp_oper = Signal(intbv(0)[16:])
    output_arp_sha = Signal(intbv(0)[48:])
    output_arp_spa = Signal(intbv(0)[32:])
    output_arp_tha = Signal(intbv(0)[48:])
    output_arp_tpa = Signal(intbv(0)[32:])
    busy = Signal(bool(0))
    error_header_early_termination = Signal(bool(0))

    # sources and sinks
    source_queue = Queue()
    source_pause = Signal(bool(0))
    sink_queue = Queue()
    sink_pause = Signal(bool(0))

    source = eth_ep.EthFrameSource(clk,
                                   rst,
                                   eth_hdr_ready=input_eth_hdr_ready,
                                   eth_hdr_valid=input_eth_hdr_valid,
                                   eth_dest_mac=input_eth_dest_mac,
                                   eth_src_mac=input_eth_src_mac,
                                   eth_type=input_eth_type,
                                   eth_payload_tdata=input_eth_payload_tdata,
                                   eth_payload_tkeep=input_eth_payload_tkeep,
                                   eth_payload_tvalid=input_eth_payload_tvalid,
                                   eth_payload_tready=input_eth_payload_tready,
                                   eth_payload_tlast=input_eth_payload_tlast,
                                   eth_payload_tuser=input_eth_payload_tuser,
                                   fifo=source_queue,
                                   pause=source_pause,
                                   name='source')

    sink = arp_ep.ARPFrameSink(clk,
                               rst,
                               frame_ready=output_frame_ready,
                               frame_valid=output_frame_valid,
                               eth_dest_mac=output_eth_dest_mac,
                               eth_src_mac=output_eth_src_mac,
                               eth_type=output_eth_type,
                               arp_htype=output_arp_htype,
                               arp_ptype=output_arp_ptype,
                               arp_hlen=output_arp_hlen,
                               arp_plen=output_arp_plen,
                               arp_oper=output_arp_oper,
                               arp_sha=output_arp_sha,
                               arp_spa=output_arp_spa,
                               arp_tha=output_arp_tha,
                               arp_tpa=output_arp_tpa,
                               fifo=sink_queue,
                               pause=sink_pause,
                               name='sink')

    # DUT
    dut = dut_arp_eth_rx_64(clk,
                          rst,
                          current_test,

                          input_eth_hdr_valid,
                          input_eth_hdr_ready,
                          input_eth_dest_mac,
                          input_eth_src_mac,
                          input_eth_type,
                          input_eth_payload_tdata,
                          input_eth_payload_tkeep,
                          input_eth_payload_tvalid,
                          input_eth_payload_tready,
                          input_eth_payload_tlast,
                          input_eth_payload_tuser,

                          output_frame_valid,
                          output_frame_ready,
                          output_eth_dest_mac,
                          output_eth_src_mac,
                          output_eth_type,
                          output_arp_htype,
                          output_arp_ptype,
                          output_arp_hlen,
                          output_arp_plen,
                          output_arp_oper,
                          output_arp_sha,
                          output_arp_spa,
                          output_arp_tha,
                          output_arp_tpa,

                          busy,
                          error_header_early_termination)

    @always(delay(4))
    def clkgen():
        clk.next = not clk

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

        yield clk.posedge

        yield clk.posedge
        print("test 1: test packet")
        current_test.next = 1

        test_frame = arp_ep.ARPFrame()
        test_frame.eth_dest_mac = 0xFFFFFFFFFFFF
        test_frame.eth_src_mac = 0x5A5152535455
        test_frame.eth_type = 0x0806
        test_frame.arp_htype = 0x0001
        test_frame.arp_ptype = 0x0800
        test_frame.arp_hlen = 6
        test_frame.arp_plen = 4
        test_frame.arp_oper = 1
        test_frame.arp_sha = 0x5A5152535455
        test_frame.arp_spa = 0xc0a80164
        test_frame.arp_tha = 0xDAD1D2D3D4D5
        test_frame.arp_tpa = 0xc0a80165
        source_queue.put(test_frame.build_eth())
        yield clk.posedge

        yield output_frame_valid.posedge
        yield clk.posedge
        yield clk.posedge

        rx_frame = None
        if not sink_queue.empty():
            rx_frame = sink_queue.get()

        assert rx_frame == test_frame

        yield delay(100)

        yield clk.posedge
        print("test 2: packet with trailing bytes")
        current_test.next = 2

        test_frame = arp_ep.ARPFrame()
        test_frame.eth_dest_mac = 0xFFFFFFFFFFFF
        test_frame.eth_src_mac = 0x5A5152535455
        test_frame.eth_type = 0x0806
        test_frame.arp_htype = 0x0001
        test_frame.arp_ptype = 0x0800
        test_frame.arp_hlen = 6
        test_frame.arp_plen = 4
        test_frame.arp_oper = 1
        test_frame.arp_sha = 0x5A5152535455
        test_frame.arp_spa = 0xc0a80164
        test_frame.arp_tha = 0xDAD1D2D3D4D5
        test_frame.arp_tpa = 0xc0a80165
        eth_frame = test_frame.build_eth()
        eth_frame.payload.data += bytearray(range(10))
        source_queue.put(eth_frame)
        yield clk.posedge

        yield output_frame_valid.posedge
        yield clk.posedge
        yield clk.posedge

        rx_frame = None
        if not sink_queue.empty():
            rx_frame = sink_queue.get()

        assert rx_frame == test_frame

        yield delay(100)

        yield clk.posedge
        print("test 3: test packet with pauses")
        current_test.next = 3

        test_frame = arp_ep.ARPFrame()
        test_frame.eth_dest_mac = 0xFFFFFFFFFFFF
        test_frame.eth_src_mac = 0x5A5152535455
        test_frame.eth_type = 0x0806
        test_frame.arp_htype = 0x0001
        test_frame.arp_ptype = 0x0800
        test_frame.arp_hlen = 6
        test_frame.arp_plen = 4
        test_frame.arp_oper = 1
        test_frame.arp_sha = 0x5A5152535455
        test_frame.arp_spa = 0xc0a80164
        test_frame.arp_tha = 0xDAD1D2D3D4D5
        test_frame.arp_tpa = 0xc0a80165
        source_queue.put(test_frame.build_eth())
        yield clk.posedge

        yield delay(16)
        yield clk.posedge
        source_pause.next = True
        yield delay(32)
        yield clk.posedge
        source_pause.next = False

        yield delay(16)
        yield clk.posedge
        sink_pause.next = True
        yield delay(32)
        yield clk.posedge
        sink_pause.next = False

        #yield output_frame_valid.posedge
        yield clk.posedge
        yield clk.posedge

        rx_frame = None
        if not sink_queue.empty():
            rx_frame = sink_queue.get()

        assert rx_frame == test_frame

        yield delay(100)

        yield clk.posedge
        print("test 4: back-to-back packets")
        current_test.next = 4

        test_frame1 = arp_ep.ARPFrame()
        test_frame1.eth_dest_mac = 0xFFFFFFFFFFFF
        test_frame1.eth_src_mac = 0x5A5152535455
        test_frame1.eth_type = 0x0806
        test_frame1.arp_htype = 0x0001
        test_frame1.arp_ptype = 0x0800
        test_frame1.arp_hlen = 6
        test_frame1.arp_plen = 4
        test_frame1.arp_oper = 1
        test_frame1.arp_sha = 0x5A5152535455
        test_frame1.arp_spa = 0xc0a80164
        test_frame1.arp_tha = 0xDAD1D2D3D4D5
        test_frame1.arp_tpa = 0xc0a80165
        test_frame2 = arp_ep.ARPFrame()
        test_frame2.eth_dest_mac = 0xFFFFFFFFFFFF
        test_frame2.eth_src_mac = 0x5A5152535455
        test_frame2.eth_type = 0x0806
        test_frame2.arp_htype = 0x0001
        test_frame2.arp_ptype = 0x0800
        test_frame2.arp_hlen = 6
        test_frame2.arp_plen = 4
        test_frame2.arp_oper = 1
        test_frame2.arp_sha = 0x5A5152535455
        test_frame2.arp_spa = 0xc0a80164
        test_frame2.arp_tha = 0xDAD1D2D3D4D5
        test_frame2.arp_tpa = 0xc0a80165
        source_queue.put(test_frame1.build_eth())
        source_queue.put(test_frame2.build_eth())
        yield clk.posedge

        yield output_frame_valid.posedge
        yield clk.posedge
        yield output_frame_valid.posedge
        yield clk.posedge
        yield clk.posedge

        rx_frame = None
        if not sink_queue.empty():
            rx_frame = sink_queue.get()

        assert rx_frame == test_frame1

        rx_frame = None
        if not sink_queue.empty():
            rx_frame = sink_queue.get()

        assert rx_frame == test_frame2

        yield delay(100)

        yield clk.posedge
        print("test 5: alternate pause source")
        current_test.next = 5

        test_frame1 = arp_ep.ARPFrame()
        test_frame1.eth_dest_mac = 0xFFFFFFFFFFFF
        test_frame1.eth_src_mac = 0x5A5152535455
        test_frame1.eth_type = 0x0806
        test_frame1.arp_htype = 0x0001
        test_frame1.arp_ptype = 0x0800
        test_frame1.arp_hlen = 6
        test_frame1.arp_plen = 4
        test_frame1.arp_oper = 1
        test_frame1.arp_sha = 0x5A5152535455
        test_frame1.arp_spa = 0xc0a80164
        test_frame1.arp_tha = 0xDAD1D2D3D4D5
        test_frame1.arp_tpa = 0xc0a80165
        test_frame2 = arp_ep.ARPFrame()
        test_frame2.eth_dest_mac = 0xFFFFFFFFFFFF
        test_frame2.eth_src_mac = 0x5A5152535455
        test_frame2.eth_type = 0x0806
        test_frame2.arp_htype = 0x0001
        test_frame2.arp_ptype = 0x0800
        test_frame2.arp_hlen = 6
        test_frame2.arp_plen = 4
        test_frame2.arp_oper = 1
        test_frame2.arp_sha = 0x5A5152535455
        test_frame2.arp_spa = 0xc0a80164
        test_frame2.arp_tha = 0xDAD1D2D3D4D5
        test_frame2.arp_tpa = 0xc0a80165
        source_queue.put(test_frame1.build_eth())
        source_queue.put(test_frame2.build_eth())
        yield clk.posedge
        yield clk.posedge

        while input_eth_payload_tvalid:
            source_pause.next = True
            yield clk.posedge
            yield clk.posedge
            yield clk.posedge
            source_pause.next = False
            yield clk.posedge

        yield clk.posedge
        yield clk.posedge

        rx_frame = None
        if not sink_queue.empty():
            rx_frame = sink_queue.get()

        assert rx_frame == test_frame1

        rx_frame = None
        if not sink_queue.empty():
            rx_frame = sink_queue.get()

        assert rx_frame == test_frame2

        yield delay(100)

        yield clk.posedge
        print("test 6: alternate pause sink")
        current_test.next = 6

        test_frame1 = arp_ep.ARPFrame()
        test_frame1.eth_dest_mac = 0xFFFFFFFFFFFF
        test_frame1.eth_src_mac = 0x5A5152535455
        test_frame1.eth_type = 0x0806
        test_frame1.arp_htype = 0x0001
        test_frame1.arp_ptype = 0x0800
        test_frame1.arp_hlen = 6
        test_frame1.arp_plen = 4
        test_frame1.arp_oper = 1
        test_frame1.arp_sha = 0x5A5152535455
        test_frame1.arp_spa = 0xc0a80164
        test_frame1.arp_tha = 0xDAD1D2D3D4D5
        test_frame1.arp_tpa = 0xc0a80165
        test_frame2 = arp_ep.ARPFrame()
        test_frame2.eth_dest_mac = 0xFFFFFFFFFFFF
        test_frame2.eth_src_mac = 0x5A5152535455
        test_frame2.eth_type = 0x0806
        test_frame2.arp_htype = 0x0001
        test_frame2.arp_ptype = 0x0800
        test_frame2.arp_hlen = 6
        test_frame2.arp_plen = 4
        test_frame2.arp_oper = 1
        test_frame2.arp_sha = 0x5A5152535455
        test_frame2.arp_spa = 0xc0a80164
        test_frame2.arp_tha = 0xDAD1D2D3D4D5
        test_frame2.arp_tpa = 0xc0a80165
        source_queue.put(test_frame1.build_eth())
        source_queue.put(test_frame2.build_eth())
        yield clk.posedge
        yield clk.posedge

        while input_eth_payload_tvalid:
            sink_pause.next = True
            yield clk.posedge
            yield clk.posedge
            yield clk.posedge
            sink_pause.next = False
            yield clk.posedge

        yield clk.posedge
        yield clk.posedge

        rx_frame = None
        if not sink_queue.empty():
            rx_frame = sink_queue.get()

        assert rx_frame == test_frame1

        rx_frame = None
        if not sink_queue.empty():
            rx_frame = sink_queue.get()

        assert rx_frame == test_frame2

        yield delay(100)

        yield clk.posedge
        print("test 7: truncated packet")
        current_test.next = 7

        test_frame = arp_ep.ARPFrame()
        test_frame.eth_dest_mac = 0xFFFFFFFFFFFF
        test_frame.eth_src_mac = 0x5A5152535455
        test_frame.eth_type = 0x0806
        test_frame.arp_htype = 0x0001
        test_frame.arp_ptype = 0x0800
        test_frame.arp_hlen = 6
        test_frame.arp_plen = 4
        test_frame.arp_oper = 1
        test_frame.arp_sha = 0x5A5152535455
        test_frame.arp_spa = 0xc0a80164
        test_frame.arp_tha = 0xDAD1D2D3D4D5
        test_frame.arp_tpa = 0xc0a80165
        eth_frame = test_frame.build_eth()
        eth_frame.payload.data = eth_frame.payload.data[:-2]
        source_queue.put(eth_frame)
        yield clk.posedge

        yield input_eth_payload_tlast.posedge
        yield clk.posedge
        yield clk.posedge
        assert error_header_early_termination

        yield delay(100)

        yield clk.posedge
        print("test 7: bad header")
        current_test.next = 7

        test_frame = arp_ep.ARPFrame()
        test_frame.eth_dest_mac = 0xFFFFFFFFFFFF
        test_frame.eth_src_mac = 0x5A5152535455
        test_frame.eth_type = 0x0806
        test_frame.arp_htype = 0x0001
        test_frame.arp_ptype = 0x0800
        test_frame.arp_hlen = 6
        test_frame.arp_plen = 4
        test_frame.arp_oper = 1
        test_frame.arp_sha = 0x5A5152535455
        test_frame.arp_spa = 0xc0a80164
        test_frame.arp_tha = 0xDAD1D2D3D4D5
        test_frame.arp_tpa = 0xc0a80165
        source_queue.put(test_frame.build_eth())
        yield clk.posedge

        yield input_eth_payload_tlast.posedge
        yield clk.posedge
        yield clk.posedge
        #assert error_header_early_termination

        yield delay(100)

        raise StopSimulation

    return dut, source, sink, clkgen, check

def test_bench():
    sim = Simulation(bench())
    sim.run()

if __name__ == '__main__':
    print("Running test...")
    test_bench()


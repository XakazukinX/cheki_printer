"""Main SP2 Interface Class."""

from .comms import SocketClientThread, ClientCommand, ClientReply
import time
import queue
import sys
import logging
from .exceptions import CommandTimedOutException, ConnectError
from .packet import PacketFactory, Packet, SpecificationsCommand, \
    VersionCommand, PrintCountCommand, ModelNameCommand, PrePrintCommand, \
    PrinterLockCommand, ResetCommand, PrepImageCommand, SendImageCommand, \
    Type83Command, Type195Command, LockStateCommand

max_trials = 1000
trial_count = 0


class SP2:
    """SP2 Client interface."""

    def __init__(self, ip='192.168.0.251', port=8080,
                 timeout=10, pinCode=1111):
        """Initialise the client."""
        logging.debug("Initialising Instax SP-2 Class")
        self.currentTimeMillis = int(round(time.time() * 1000))
        self.ip = ip
        self.port = port
        self.timeout = 10
        self.pinCode = pinCode
        self.packetFactory = PacketFactory()

    def connect(self):
        """Connect to a printer."""
        logging.debug("Connecting to Instax SP-2 with timeout of: %s" % self.timeout)
        self.comms = SocketClientThread()
        # main Threadが死んだら別スレッドも死ぬようにする
        # pythonのThread周りよくわからんのでいつか調べる(いつか)
        self.comms.daemon = True
        self.comms.start()
        self.comms.cmd_q.put(ClientCommand(ClientCommand.CONNECT,
                                           [self.ip, self.port]))
        # Get current time
        start = int(time.time())
        while int(time.time()) < (start + self.timeout):
            try:
                reply = self.comms.reply_q.get(False)
                if reply.type == ClientReply.SUCCESS:
                    return
                else:
                    raise (ConnectError(reply.data))
            except queue.Empty:
                time.sleep(0.1)
            except ConnectError as err:
                print("[エラー] 接続時にエラーが発生しました。 %s" % err)
                return err
        else:
            raise (CommandTimedOutException())

    def send_and_recieve(self, cmdBytes, timeout):
        """Send a command and waits for a response.

        This is a blocking call and will not check that the response is
        the correct command type for the command.
        """
        self.comms.cmd_q.put(ClientCommand(ClientCommand.SEND, cmdBytes))
        self.comms.cmd_q.put(ClientCommand(ClientCommand.RECEIVE))

        # Get current time
        start = int(time.time())
        while (int(time.time()) < (start + timeout)):
            try:
                reply = self.comms.reply_q.get(False)
                if reply.data is not None:
                    if reply.type == ClientReply.SUCCESS:
                        return reply
                    else:
                        raise (ConnectError(reply.data))
            except queue.Empty:
                time.sleep(0.1)
                pass
        raise (CommandTimedOutException())

    def sendCommand(self, commandPacket):
        """Send a command packet and returns the response."""
        try:
            encodedPacket = commandPacket.encodeCommand(self.currentTimeMillis, self.pinCode)
            decodedCommand = self.packetFactory.decode(encodedPacket)
            decodedCommand.printDebug()
            reply = self.send_and_recieve(encodedPacket, 5)
            decodedResponse = self.packetFactory.decode(reply.data)
        except Exception as err:
            print("[エラー] AAAAA %s" % err)
            raise err
        decodedResponse.printDebug()

        return decodedResponse

    def getPrinterVersion(self):
        """Get the version of the Printer hardware."""
        cmdPacket = VersionCommand(Packet.MESSAGE_MODE_COMMAND)
        response = self.sendCommand(cmdPacket)
        return response

    def getPrinterModelName(self):
        """Get the Model Name of the Printer."""
        cmdPacket = ModelNameCommand(Packet.MESSAGE_MODE_COMMAND)
        response = self.sendCommand(cmdPacket)
        return response

    def getPrintCount(self):
        """Get the historical number of prints."""
        cmdPacket = PrintCountCommand(Packet.MESSAGE_MODE_COMMAND)
        response = self.sendCommand(cmdPacket)
        return response

    def getPrinterSpecifications(self):
        """Get the printer specifications."""
        cmdPacket = SpecificationsCommand(Packet.MESSAGE_MODE_COMMAND)
        response = self.sendCommand(cmdPacket)
        return response

    def sendPrePrintCommand(self, cmdNumber):
        """Send a PrePrint Command."""
        cmdPacket = PrePrintCommand(Packet.MESSAGE_MODE_COMMAND,
                                    cmdNumber=cmdNumber)
        response = self.sendCommand(cmdPacket)
        return response

    def sendLockCommand(self, lockState):
        """Send a Lock State Commmand."""
        cmdPacket = PrinterLockCommand(Packet.MESSAGE_MODE_COMMAND,
                                       lockState=lockState)
        response = self.sendCommand(cmdPacket)
        return response

    def sendResetCommand(self):
        """Send a Reset Command."""
        cmdPacket = ResetCommand(Packet.MESSAGE_MODE_COMMAND)
        response = self.sendCommand(cmdPacket)
        return response

    def sendPrepImageCommand(self, format, options, imgLength):
        """Send a Prep for Image Command."""
        cmdPacket = PrepImageCommand(Packet.MESSAGE_MODE_COMMAND,
                                     format=format,
                                     options=options,
                                     imgLength=imgLength)
        response = self.sendCommand(cmdPacket)
        return response

    def sendSendImageCommand(self, sequenceNumber, payloadBytes):
        """Send an Image Segment Command."""
        cmdPacket = SendImageCommand(Packet.MESSAGE_MODE_COMMAND,
                                     sequenceNumber=sequenceNumber,
                                     payloadBytes=payloadBytes)
        response = self.sendCommand(cmdPacket)
        return response

    def sendT83Command(self):
        """Send a Type 83 Command."""
        cmdPacket = Type83Command(Packet.MESSAGE_MODE_COMMAND)
        response = self.sendCommand(cmdPacket)
        return response

    def sendT195Command(self):
        """Send a Type 195 Command."""
        cmdPacket = Type195Command(Packet.MESSAGE_MODE_COMMAND)
        response = self.sendCommand(cmdPacket)
        return response

    def sendLockStateCommand(self):
        """Send a LockState Command."""
        cmdPacket = LockStateCommand(Packet.MESSAGE_MODE_COMMAND)
        response = self.sendCommand(cmdPacket)
        return response

    def close(self, timeout=10):
        """Close the connection to the Printer."""
        logging.debug("Closing connection to Instax SP2")
        self.comms.cmd_q.put(ClientCommand(ClientCommand.CLOSE))
        # Get current time
        start = int(time.time())
        while (int(time.time()) < (start + timeout)):
            try:
                reply = self.comms.reply_q.get(False)
                if reply.type == ClientReply.SUCCESS:
                    self.comms.join()
                    self.comms = None
                    return
                else:
                    raise (ConnectError(reply.data))
            except queue.Empty:
                time.sleep(0.1)
                pass
        self.comms.join()
        self.comms = None
        raise (CommandTimedOutException())

    def getPrinterInformation(self):
        """Primary function to get SP-2 information."""
        self.connect()
        printerVersion = self.getPrinterVersion()
        printerModel = self.getPrinterModelName()
        printerSpecifications = self.getPrinterSpecifications()
        printCount = self.getPrintCount()
        printerInformation = {
            'version': printerVersion.payload,
            'model': printerModel.payload['modelName'],
            'battery': printerVersion.header['battery'],
            'printCount': printerVersion.header['printCount'],
            'specs': printerSpecifications.payload,
            'count': printCount.payload['printHistory']
        }
        self.close()
        return printerInformation

    def printPhoto(self, imageBytes, progress):
        global max_trials
        global trial_count

        """Print a Photo to the Printer."""
        progressTotal = 100
        progress(0, progressTotal, status='Connecting to instax Printer.           ')
        # Send Pre Print Commands
        err = self.connect()
        if err is not None:
            progress(100, progressTotal, status='Print is Failed!                       \n')
            trial_count += 1
            if trial_count < max_trials:
                print("再接続します")
                err = self.printPhoto(imageBytes, progress)
                if err is not None:
                    return err
            else:
                return err
        progress(10, progressTotal, status='Connected! - Sending Pre Print Commands.')
        time.sleep(1)
        try:
            for x in range(1, 9):
                self.sendPrePrintCommand(x)
            self.close()

            # Lock The Printer
            time.sleep(1)
            self.connect()
            progress(20, progressTotal, status='Locking Printer for Print.               ')
            self.sendLockCommand(1)
            self.close()

            # Reset the Printer
            time.sleep(1)
            self.connect()
            progress(30, progressTotal, status='Resetting Printer.                         ')
            self.sendResetCommand()
            self.close()
            # Send the Image
            time.sleep(1)
            self.connect()
            progress(40, progressTotal, status='About to send Image.                       ')
            self.sendPrepImageCommand(16, 0, 1440000)
            for segment in range(24):
                start = segment * 60000
                end = start + 60000
                segmentBytes = imageBytes[start:end]
                self.sendSendImageCommand(segment, bytes(segmentBytes))
                progress(40 + segment, progressTotal, status=('Sent image segment %s.         ' % segment))
            self.sendT83Command()
            self.close()
            progress(70, progressTotal, status='Image Print Started.                       ')
            # Send Print State Req
            time.sleep(1)
            self.connect()
            self.sendLockStateCommand()
            self.getPrinterVersion()
            self.getPrinterModelName()
        except Exception as err:
            progress(100, progressTotal, status='Print is Failed!                       \n')
            trial_count += 1
            if trial_count < max_trials:
                print("再送します")
                self.sendResetCommand()
                err = self.printPhoto(imageBytes, progress)
                if err is not None:
                    return err
                else:
                    return err
            print("[エラー] !!!! %s" % err)

        progress(90, progressTotal, status='Checking status of print.                    ')
        printStatus = self.checkPrintStatus(30)
        if printStatus is True:
            progress(100, progressTotal, status='Print is complete!                       \n')
        else:
            progress(100, progressTotal, status='Timed out waiting for print..            \n')
        self.sendResetCommand()
        self.close()

    def checkPrintStatus(self, timeout=30):
        """Check the status of a print."""
        for _ in range(timeout):
            printStateCmd = self.sendT195Command()
            if printStateCmd.header['returnCode'] is Packet.RTN_E_RCV_FRAME:
                return True
            else:
                time.sleep(1)
        return False

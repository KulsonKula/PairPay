import React from "react";
import { Modal, ModalContent, ModalHeader, ModalBody, ModalFooter, Button, useDisclosure } from "@nextui-org/react";
import { Navbar, NavbarContent, NavbarItem, Link } from "@nextui-org/react";
import im from './backimage.jpg';

export default function App() {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [activeModal, setActiveModal] = React.useState(null);
  const [backdrop, setBackdrop] = React.useState("opaque");

  const modals = [
    { name: "bills", title: "Rachunki", content: "Stwórz nowy rachunek, dodaj wydatki oraz uczestników. Podział kosztów zrobimy za Ciebie." },
    { name: "groups", title: "Grupy", content: "Stwórz grupy znajomych i uprość sobie tworzenie rachunków." },
    { name: "account", title: "Moje konto", content: "Zobacz informacje o swoim koncie." },
  ];

  const handleOpen = (modalName) => {
    setActiveModal(modalName);
    setBackdrop("blur");
    onOpen();
  };

  const handleClose = () => {
    setActiveModal(null);
    onClose();
  };

  return (
    <>
      <Navbar isBordered isBlurred={false} className="sticky top-0 bg-primary-100 z-50">
        <NavbarContent className="mx-auto max-w-screen-lg" justify="front">
          <NavbarItem>
            <Link color="foreground" href="#">
              Strona główna
            </Link>
          </NavbarItem>
          <NavbarItem>
            <Link color="foreground" href="#">
              Rachunki
            </Link>
          </NavbarItem>
          <NavbarItem>
            <Link href="#" color="foreground">
              Grupy
            </Link>
          </NavbarItem>
          <NavbarItem>
            <Link color="foreground" href="#">
              Moje konto
            </Link>
          </NavbarItem>
        </NavbarContent>

        <NavbarContent justify="end">
          <NavbarItem className="hidden lg:flex">
            <Link href="/login">
            </Link>
          </NavbarItem>
          <NavbarItem>
            <Button as={Link} color="primary" href="/login" variant="flat">
              Login
            </Button>
          </NavbarItem>
        </NavbarContent>

      </Navbar>

      <div className="relative w-full h-screen bg-cover bg-center" style={{ backgroundImage: `url(${im})` }}>
        <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-b from-transparent to-black z-0"></div>
        <div className="relative z-10 flex flex-col items-center justify-center pt-24">
          <h2 className="text-8xl font-bold text-light-100 mb-4 font-serif">PairPay</h2>
          <h3 className="text-2xl font-bold text-light-100 mb-8 font-serif">Nie martw się o podział kosztów</h3>
        </div>
      </div>

      <div className="flex flex-col items-center justify-start min-h-[50vh] pt-16 bg-background">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {modals.map((modal) => (
            <div
              key={modal.name}
              onClick={() => handleOpen(modal.name)}
              className="cursor-pointer bg-primary-100 hover:bg-gradient-to-r from-cyan-600 to-blue-600 w-100 h-60 shadow-lg p-6 rounded-lg transition-all duration-300"
            >
              <h3 className="text-xl font-bold text-primary-800 mb-2">{modal.title}</h3>
              <p className="text-sm text-primary-600">{modal.content.substring(0, 60)}...</p>
            </div>
          ))}
        </div>


        {modals.map(
          (modal) =>
            activeModal === modal.name && (
              <Modal
                key={modal.name}
                backdrop={backdrop}
                isOpen={isOpen}
                onClose={handleClose}
                className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-50 mt-10"
              >
                <ModalContent className="bg-gradient-to-r from-cyan-600 to-blue-600">
                  <ModalHeader className="flex flex-col gap-1">PairPay</ModalHeader>
                  <ModalBody>
                    <div className="mb-4">
                      <h3 className="text-lg font-semibold">{modal.title}</h3>
                      <p>{modal.content}</p>
                    </div>
                  </ModalBody>
                  <ModalFooter>
                    <Button className="cursor-pointer bg-primary-600 hover:bg-primary-300 text-white"  onPress={handleClose}>
                      Zamknij
                    </Button>
                    <Button className="cursor-pointer bg-primary-600 hover:bg-primary-300 text-white" onPress={handleClose}>
                      Dowiedz się więcej
                    </Button>
                  </ModalFooter>
                </ModalContent>
              </Modal>
            )
        )}
      </div>
    </>
  );
}
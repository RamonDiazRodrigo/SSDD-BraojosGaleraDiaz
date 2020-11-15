module GestionMapas {

  exception Unauthorized {};
  exception RoomAlreadyExists{};
  exception RoomNotExists{};
  
  interface GestMapas {
    void publish(string token, string roomData) throws Unauthorized, RoomNotExists;
    void remove(string token, string roomName) throws RoomNotExists;
  };
  
};

# PMDB
- Program management discord bot
- 원하는 CLI 프로그램을 디스코드를 통해 관리하도록 도와주는 디스코드 봇입니다

### How to use
- 원하는 프로그램 실행 파일이 있는 폴더에 Bot 폴더의 내용물을 넣습니다
- Main.py와 서버 실행기를 파이프로 이어 실행합니다
- ex) python Main.py | ./server.exe

### Feature
- 프로그램에 집적적으로 명령어 전송
- 프로그램 출력 로그를 봇을 통해 확인(WIP)
- 봇을 통한 프로그램 on/off(WIP)
- 클라우드 플랫폼 사용시 봇을 통한 인스턴스 on/off(WIP)

### TODO
- [ ] 프로그램과 봇이 독립적으로 동작할 수 있도록 직접 파이프로 연결하지 않고 named pipe와 같은 IPC를 사용해 통신하도록 변경
  - [ ] 실행 프로그램에 붙어 입/출력을 IPC를 통해 봇과 연결해주는 attacher 제작

- [ ] 프로그램과 봇이 다른 컴퓨터간에도 관리 가능하게 소켓 통신 적용

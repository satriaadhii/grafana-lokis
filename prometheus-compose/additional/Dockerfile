FROM alpine
COPY ./cpu-top.sh ./memory-top.sh /
RUN chmod +x /cpu-top.sh /memory-top.sh
RUN apk add --no-cache --upgrade bash
RUN apk add --no-cache --upgrade curl
CMD [ "ps" ]
